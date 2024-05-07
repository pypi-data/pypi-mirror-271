import sys
from datetime import datetime
from typing import Optional

from BdrcDbLib.DbAppParser import DbAppParser, str2datetime, DbArgNamespace
from BdrcDbLib.DbApp import DbApp

# Constants
from util_lib.version import ver_check

from util_lib.utils import reallypath

DIP_ID_KEY: str = "DIP_ACTIVITY_ID"


class DipLogParser(DbAppParser):
    # noinspection PyTypeChecker
    def __init__(self, description: str, usage: str):
        """
        Constructor. Sets up the arguments for
        INSERT INTO `drs`.`dip_activity`
        (
        `dip_activity_type_id`,
        `dip_activity_start`,
        `dip_activity_end`,
        `dip_activity_success`,
        `dip_source_path`,
        `dip_dest_path`,

        `dip_external_id`)

        """

        src_path_help: str = "Source path (optional) - string"
        dest_path_help: str = "Destination path (optional) - string"

        super().__init__(description, usage)
        self._parser.add_argument("-l", "--log-level", dest='log_level', action='store',
                                  choices=['info', 'warning', 'error', 'debug', 'critical'], default='info',
                                  help="choice values are from python logging module")

        self._parser.add_argument("-a", "--activity_type", help="Activity type",

                                  required=False)

        self._parser.add_argument("-w", "--work_name", help="work being distributed", required=False)
        self._parser.add_argument("-i", "--dip_id", help="ID to update", required=False)
        self._parser.add_argument("-r", "--activity_return_code", help="Integer result of operation.", type=int,
                                  required=False)
        self._parser.add_argument("-b", "--begin_time", help="time of beginning - ')"
                                                             "yyyy-mm-dd hh:mm:ss bash format date +\'%%Y-%%m-%%d "
                                                             "%%R:%%S\'",
                                  required=False, type=str2datetime)
        self._parser.add_argument("-e", "--end_time", help="time of end.Default is invocation time. "
                                                           "yyyy-mm-dd hh:mm:ss bash format date + \'%%Y-%%m-%%d "
                                                           "%%R:%%S\'",
                                  required=False, type=str2datetime)
        self._parser.add_argument("-c", "--comment", help="Any text up to 4GB in length", required=False)
        self._parser.add_argument("-s", "--dip_source_path", help=src_path_help, required=False)
        self._parser.add_argument("-t", "--dip_dest_path", help=dest_path_help, required=False)
        self._parser.add_argument("-L", "--resolve-sym-links",
                                  help="True to resolve file paths, false to accept input as is", required=False,
                                  default=False, action='store_true')
        self._parser.add_argument("source_path", help=src_path_help, nargs='?')
        self._parser.add_argument("dest_path", help=dest_path_help, nargs='?')

        self.validate()

        self.adjust_begin()

    def validate(self):
        """
        Test Arguments
        :return: Nothing. Raise ValueError if invalid args
        """
        pa: DbArgNamespace = self.parsedArgs

        # You can refer to the work either by the tuple of (.activity_type, .work_name, .begin_time) OR
        # .dip_id.
        # TODO: What if you use both .dip_id and (.activity_type, .work_name, .begin_time)

        if not pa.dip_id:
            if not pa.begin_time \
                    or not pa.work_name \
                    or not pa.activity_type:
                raise ValueError(
                    "LOG_DIP: When --dip_id is not given, --begin_time, --work_name, and --activity_type must be "
                    "given.")

        if pa.end_time is not None and pa.begin_time is not None and pa.end_time < pa.begin_time:
            raise ValueError("LOG_DIP: end time before begin time")

        # If the positional arguments were given, and the flag arguments were not, copy the positionals
        # into the flag arguments
        # Handle "-s sArgGiven" positionalFileArgGiven --> dest gets positional File Arg

        # archive-ops-1060: For docker, we can't use the hardcoded default db descriptor, we must use the one
        # that the user provides on the command line to get the current set of activities. This stanza moves
        # the arg activities validation here, after the db config is parsed.
        if pa.activity_type:
            rpa = pa.activity_type.upper()
            allowed_activities:[] = [x.upper() for x in self.activities(pa.drsDbConfig)]
            if rpa not in allowed_activities:
                raise ValueError(f"LOG_DIP: activity_type {rpa} must be one of {allowed_activities}")


        if pa.dip_source_path is not None and pa.dip_dest_path is None and pa.dest_path is None:
            pa.dip_dest_path = pa.source_path

        if pa.dip_source_path is None and pa.source_path is not None:
            pa.dip_source_path = pa.source_path
        if pa.dip_dest_path is None and pa.dest_path is not None:
            pa.dip_dest_path = pa.dest_path

        if pa.resolve_sym_links:
            pa.dip_source_path = reallypath(pa.dip_source_path)
            pa.dip_dest_path = reallypath(pa.dip_dest_path)

    def adjust_begin(self):
        """
            Cleanup for beginning and end times. ???
            """
        pa: DbArgNamespace = self.parsedArgs
        has_begin: bool = pa.begin_time is not None
        has_end: bool = pa.end_time is not None
        has_id: bool = pa.dip_id is not None

        # rules:  if begin, don't need end or id.
        # you have to have an id when:
        #   - ending
        #   - no beginning?
        if has_end and not has_begin and not has_id:
            self._parser.error("end time requires begin time or id")

    def activities(self, db_config:str) -> [str]:
        """
        Legal list of activities
        :param db_config: BDRC database configuration
        :return:
        """
        from BdrcDbLib.DbOrm.DrsContextBase import DrsDbContextBase
        from BdrcDbLib.DbOrm.models.drs import DipActivities
        labels: [] = []

        with DrsDbContextBase(db_config) as ctx:
            labels = [x[0] for x in ctx.session.query(DipActivities.label).all()]
        return labels


class DipLog(DbApp):
    """
    Send a log entry to the database
    """

    def __init__(self, db_config: str):
        super().__init__(db_config)

    def set_dip(self, activity_name: Optional[str] ,
                begin_t: Optional[datetime] ,
                end_t: Optional[datetime] ,
                s_path: Optional[str] ,
                d_path: Optional[str] ,
                work_name: Optional[str] ,
                dip_id: Optional[str] ,
                ac_result: Optional[int] ,
                comment: Optional[str]) -> str:
        """
        Call the SQL and retrieve the dip activity ID it generated :param activity_name: the type of activity (e.g.
        BUDA, DEEP_ARCHIVE) :param begin_t: begin time :param end_t: end time or null :param s_path: source path
        :param activity_name: a value in dip_activity_types.dip_activity_types_label
        :param begin_t: begin time
        :param end_t: end time
        :param s_path: source path
        :param d_path: destination path
        :param work_name: workRID
        :param dip_id: NONE to create a new DIP log entry
        if an existing (work_name, start_time, activity_name) is given , the SPROC updates it and returns the
        existing dip_id
        :param ac_result: result of operation, if known.
        :param comment: Any extra text
        :return: The value of DIP_ACTIVITY_ID from the result set returned
        """
        # protect call against SQL 1213 Deadlock found when trying to get lock; try restarting transaction

        query_result_list: list[dict] = self.CallAnySproc('SetWorkDip', work_name, begin_t, end_t, activity_name,
                                                          ac_result, s_path, d_path,
                                                          dip_id, comment)
        # Query result is a list of lists of dictionary entries
        activity_id: str = ""
        for rs_list in query_result_list:
            for ww in rs_list:
                if DIP_ID_KEY in ww.keys():
                    activity_id = ww[DIP_ID_KEY]
                    break
            if len(activity_id) > 0:
                break

        return activity_id


def dip_log_shell() -> None:
    """
    Intended for use with shell.
    Ex:  bash
    DIP_ID=$(log_dip -d ... -b .... -e ....)
    :return: DIP_ID operated on
    """
    exit_rc = 0
    ver_check()

    try:
        dlp = DipLogParser("Logs a number of different publication strategies",
                           "log_dip [OPTIONS] [dip_source_path] [dip_dest_path]  ")
        dla: DbArgNamespace = dlp.parsedArgs
        dl: DipLog = DipLog(dla.drsDbConfig)

        print(dl.set_dip(dla.activity_type, dla.begin_time, dla.end_time, dla.dip_source_path,
                         dla.dip_dest_path,
                         dla.work_name, dla.dip_id, dla.activity_return_code, dla.comment))
    except ValueError:
        ei = sys.exc_info()
        print(str(ei[1]))
        exit_rc = 1

    sys.exit(exit_rc)


if __name__ == "__main__":
    dip_log_shell()
