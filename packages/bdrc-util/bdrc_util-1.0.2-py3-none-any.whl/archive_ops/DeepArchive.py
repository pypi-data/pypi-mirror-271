#!/usr/bin/env python3
"""
Replacement for scripts/glacier/DIP-pump-uploadWorkToGlacier.py

What this routine produces depends if we are only uploading the media in a set of image groups, or the complete work.
this is driven by the third column of the input file, which may contain a regex that identifies the image groups to upload:
the regex is DA_UPLOADS/(.*)/DA_UPLOADS and the contents (.*) are a comma separated list of image groups to upload.
If the comment field is present, only the image groups in the comment field are uploaded.
If not present:
- each image group is inverted and uploaded into its own bag.zip
- everything else is assembled into its own bag.zip, which is named after the work_rid
"""
# import sys
# print(sys.path)
# import os
# print(os.environ['PYTHONPATH'])
      
import datetime
from collections import namedtuple
from tempfile import TemporaryDirectory
from typing import Optional, Union, List
from pathlib import Path

from s3pathlib import S3Path

import archive_ops.InvertWorkException
from archive_ops.DeepArchiveParser import DeepArchiveParser, DeepArchiveArgs
from archive_ops.InvertWork import get_igs_for_invert, get_media_splits, invert_image_group_media

import archive_ops.api as AoApi

from util_lib.AOLogger import AOLogger
from util_lib.utils import *
from archive_ops.DipLog import DipLog

PROD_BUCKET: str = 'glacier.archive.bdrc.org'
DEV_BUCKET: str = 'manifest.bdrc.org'
CUR_BUCKET: str = PROD_BUCKET
#
# Format that doOneWork *may* in the future, use to specify
# the specific image groups in a sync. see get_igs_for_invert
IN_COMMENT_RE: str = r".*DA_IMAGE_GROUPS/(.*)/DA_IMAGE_GROUPS.*"

GLACIER_KEY_ROOT: str = 'Archive'
BAGZIP_SUFFIX: str = '.bag.zip'

# -----------------     globals  -------------------
# noinspection PyTypeChecker
_log: AOLogger = None
# noinspection PyTypeChecker
dip_logger: DipLog = None

# This describes the fields in the results of GetDIPActivityCandidates.sql as
# written by get_works_for_activity
HEADERS = ['WorkName', 'path', 'dip_comment']
InputDirectiveRow = namedtuple('Todo', HEADERS)  # Create a named tuple type


# -----------------     /globals  -------------------


def do_deep_archive(work_rid: str, archive_path: Path, image_groups: [str], only_do_image_groups: bool) -> int:
    """
    Splits a work archive
    :param work_rid:
    :param archive_path: data source
    :param image_groups: list of image groups to process
    :param only_do_image_groups: if true, only the image groups in the comment are processed, otherwise, create
    a separate zip file containing everything not in the image groups.
    :return:
    """
    # Get s3 archive home, under the key. See archive-ops/scripts/glacier/DIP-pump-uploadWorkToGlacier.sh

    work_tag: {} = AOS3WorkTag(work_rid).extra_args_tag

    # Different algorithm. We need to divide the work into two sets: 1 for the image groups which
    # are to be inverted, the other into a set of directories that will be copied as is.
    #
    media_with_image_group, non_image_groups = get_media_splits(archive_path, image_groups)

    for ig, media_dirs in media_with_image_group.items():
        do_bag_upload(archive_path=archive_path, work_rid=work_rid, work_tag=work_tag, invert_context=(ig, media_dirs))

    if non_image_groups and not only_do_image_groups:
        do_bag_upload(archive_path=archive_path, work_rid=work_rid, work_tag=work_tag, as_is=non_image_groups)

    return 0


def do_bag_upload(archive_path: str, work_rid: str, work_tag: str, invert_context: () = None, as_is: [str] = None):
    """
    create a bag.zip for the image group and upload it to the archive
    :param archive_path:
    :param image_group:
    :param media_with_image_group:
    :param work_rid:
    :param work_tag:
    :return:
    """
    import shutil
    from bdrc_bag.bag_ops import bag

    if invert_context:
        dest_name, media_with_image_group = invert_context
    else:
        dest_name = work_rid

    s3_parent: S3Path = S3Path(CUR_BUCKET, AoApi.get_archive_location(GLACIER_KEY_ROOT, work_rid))
    # Make a temporary path for the output:
    with (TemporaryDirectory() as out_buffer):
        dip_id: str = ""
        failed_item_message: str = ""
        had_fail: bool = False
        ig_dest_path: S3Path = s3_parent / f"{dest_name}{BAGZIP_SUFFIX}"
        try:
            dip_id = open_log_dip(work_rid, archive_path, ig_dest_path.arn)
            out_path = Path(out_buffer)
            dest_path: Path = out_path / dest_name
            dest_path.mkdir(parents=True, exist_ok=True)
            ips: str = str(dest_path)
            bag_path: Path = out_path / "bag" / dest_name
            bag_path.mkdir(parents=True, exist_ok=True)
            bps: str = str(bag_path)

            # Invert the image group into the temp directory's work_folder
            if invert_context:
                invert_image_group_media(dest_path, media_with_image_group, dest_name)
            else:
                # Just copy the directories
                for dir_name in as_is:
                    complete_sub_path = dest_path / children_of(dir_name, work_rid)
                    complete_sub_path.mkdir(parents=True, exist_ok=True)
                    shutil.copytree(dir_name, complete_sub_path, dirs_exist_ok=True)
            bag(ips, bps, False, False, False)

            # Upload the inversion(s) to the archive. In this workflow, there should only be one
            for root, dirs, files in os.walk(bag_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    #
                    # Handle subdirs by removing the top of tree
                    s3_object_name = file_path.replace(bps, "", 1).lstrip(os.sep)
                    s3_target: S3Path = s3_parent / s3_object_name
                    upload_file_to_s3_with_storage_class(file_path, s3_target.bucket, s3_target.key, 'STANDARD_IA',
                                                         work_tag)
        except Exception as e:
            failed_item_message = f"failed deep_archive {work_rid=} {dest_path=} {e=}"
            _log.exception(e)
            had_fail = True
        finally:
            if dip_id:
                update_log_dip(dip_id, 1 if had_fail else 0, failed_item_message)
            if had_fail:
                complain(f"{work_rid=}, {failed_item_message=}", 1, "do_deep_archive")


def children_of(anchor: str, a_path: str) -> Path:
    """
    Returns a path relative to the work_rid in dir_name
    :param a_path:
    :param anchor:
    :return:
    """
    dir_path = Path(anchor)
    _d_parts = dir_path.parts
    _w_sub = _d_parts.index(a_path)
    sub_path = Path(*_d_parts[_w_sub + 1:])
    return sub_path


def upload_file_to_s3_with_storage_class(file_name, bucket, key=None, storage_class='STANDARD',
                                         tag_set: Optional[str] = None):
    """Upload a file to an S3 bucket with a specific storage class

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param key: S3 object name. If not specified then file_name is used
    :param storage_class: Storage class to use for the object
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if key is None:
        key = file_name

    # Upload the file
    import boto3
    s3_client = boto3.client('s3')
    from botocore.exceptions import ClientError
    try:

        # handy: Can set tagging here:
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.put_object_tagging
        extra_args: {} = {'StorageClass': storage_class}
        if tag_set:
            # __/|\__ gh copilot
            extra_args.update(tag_set)
        import json
        extra_arg_string = json.dumps(extra_args)
        s3_client.upload_file(file_name, bucket, key, ExtraArgs=extra_args)
    except ClientError as e:
        _log.exception(e)
        return False
    return True


def setup(args: DeepArchiveArgs):
    """
    Open resources
    :return: sets logger and dip_log context
    """

    import os
    global _log
    global dip_logger

    if not _log:
        os.makedirs(args.log_root, exist_ok=True)
        _log = AOLogger("Deep_Archive", args.log_level, Path(args.log_root), extra_quiet_loggers=['bagit'])
    if not dip_logger:
        import os
        # Need different path under docker
        db_cfg: [str] = args.drsDbConfig.split(':')

        # Still need to check, in case not run through argparse (i.e. db_config manually populated)
        if len(db_cfg) < 2:
            raise ValueError(f"Invalid db config {args.drsDbConfig} requires section:configFileName")

        # Adjust for running under docker - should be part of DbApps
        db_cfg[1] = '/run/secrets/db_apps' if os.path.exists('/run/secrets') else db_cfg[1]
        args.drsDbConfig = ':'.join(db_cfg)
        dip_logger = DipLog(args.drsDbConfig)


def displayed_comment(displayed, display_length: int = 108, illus_len: int = 20) -> str:
    """
    if displayed is > 108, trim to [1:20]"..."[-20:]
    :param display_length: invocation threshold
    :param illus_len:

    :param displayed:
    :return:
    """
    return f"{displayed[:illus_len]}...{displayed[-illus_len:]}" if len(displayed) > display_length else displayed


def update_log_dip(dip_log_id: str,
                   rc: int,
                   comment: str,
                   src_path: Optional[str] = None,
                   dest_path: Optional[str] = None,
                   ):
    """
    Closes a dip log entry
    :param dip_log_id: Key to locate entry
    :param comment: goes into database
    :param rc: activity return code for log
    :param src_path: source path (shouldn't usually update)
    :param dest_path: output path
    :return:
    """
    log_comment = displayed_comment(comment)
    _log.info(f'closing :{dip_log_id=}\trc:{rc=} {log_comment=}')
    return dip_logger.set_dip(
        # These are table PKs  - you can't update them
        activity_name=None,
        begin_t=None,
        work_name=None,
        # end keys
        # this is the identifying key
        dip_id=dip_log_id,
        # Tell the truth now
        end_t=datetime.datetime.now(),
        # The rest of these are optional
        s_path=src_path,
        d_path=dest_path,
        ac_result=rc,
        comment=comment)


def open_log_dip(work_rid: str, src_path: str, aws_object_path: Optional[str] = None) -> str:
    """
    Opens a dip log entry
    :return:
    :param work_rid: Key to locate entry
    :param src_path: goes into database
    :param aws_object_path: return code to log
    :return: dip_log_id
    """
    global dip_logger
    _log.info(f'opening :{work_rid=}\t{src_path=}\t{aws_object_path=}')

    # set_dip has no optional args:
    return dip_logger.set_dip(activity_name='DEEP_ARCHIVE',
                              begin_t=datetime.datetime.now(),
                              end_t=None,
                              s_path=src_path,
                              d_path=aws_object_path,
                              dip_id=None,
                              work_name=work_rid,
                              ac_result=None,
                              comment=None)


# send a message to an AWS SNS topic
def send_sns(subject: str, message_str):
    """
    Send a message to an AWS SNS topic
    :return:
    """
    import os
    topic: str = os.getenv('AO_AWS_SNS_TOPIC_ARN')
    if topic:
        # Usually configured for default
        import boto3
        sns = boto3.client('sns').publish(TopicArn=topic, Message=message_str,
                                          Subject=subject)
    _log.info(f'{"[sns]" if topic else "[log]"} {subject}, {message_str}')


def complain(object_tag: str, rc: int, operation_tag: str, detail: str = None):
    d4_fstring = f"with {detail=}" if detail else ''""
    sns_fails_message_string = f"""
    The following work could not be uploaded to Glacier:
    {object_tag}.
    {operation_tag} returned with exit code {rc} {d4_fstring}
    """

    send_sns("Glacier Upload Failure Report", sns_fails_message_string)


def get_header_indices(header: [str], columns: [str]) -> ():
    return tuple(map(lambda x: header.index(x), columns))


def read_csv(csv_path: Path) -> [InputDirectiveRow]:
    """
    Map a csv file into a list of named tuples Note the packager has
    to be sure to escape any commas in the comment field"
    """
    import csv
    with open(csv_path, 'r') as f:
        reader = csv.reader(f)  # Skip the header
        header = next(reader)

        h_map = get_header_indices(header, HEADERS)
        records: [InputDirectiveRow] = [InputDirectiveRow(*(row[i] for i in h_map)) for row in reader]
        # noinspection PyTypeChecker
        _log.debug(records)
        return records


def deep_archive_cli():
    """
    Command line interface
    :return:
    """
    da_parser: DeepArchiveParser = DeepArchiveParser(usage="%(prog)s -i input_file",
                                                     description="Uploads a series of inverted zip files to backup "
                                                                 "bucket", )

    args: DeepArchiveArgs = da_parser.parsedArgs
    setup(args)
    _log.info(f"Arguments: {str(args)}")

    CUR_BUCKET = PROD_BUCKET if args.drsDbConfig.split(':')[0] == 'prod' else DEV_BUCKET

    _log.info(f"Using {CUR_BUCKET=}")

    records: [InputDirectiveRow] = read_csv(args.input_file)
    for record in records:
        try:
            image_group_list, comment_was_source = get_igs_for_invert(record.WorkName, record.path, IN_COMMENT_RE,
                                                                      record.dip_comment)
            #
            # if there was a comment, we're only doing the image groups that were designated in the comment.
            # Otherwise, segment the work into:
            # - imagegroup + media tuples to be inverted and zipped separately
            # - everything else
            do_deep_archive(record.WorkName, Path(record.path), image_group_list, comment_was_source)
            _log.info(f"Processing {record}")
        except archive_ops.InvertWorkException.InvertWorkException as e:
            dip_id = open_log_dip(record.WorkName, record.path)
            error_string: str = f"Failed to process {record=} {dip_id=} Exception {e=}"
            _log.error(error_string)
            update_log_dip(dip_id, 1, error_string)
            complain(record.WorkName, 1, "deep_archive_cli", error_string)


if __name__ == '__main__':
    deep_archive_cli()
