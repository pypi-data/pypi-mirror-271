#!/usr/bin/env python3
import os
from argparse import Namespace

from BdrcDbLib.DbAppParser import DbAppParser


class DeepArchiveArgs:
    """
    For IDE usage - define the arg namespace, but in a way that allows
    export to other libs: See the DeepArchiveParser class and superclass.
    Any attribute not defined here, and added by the parser can be considered
    as "_private"
    """
    def __init__(self):
        self.log_level = None
        self.log_root = None
        self.input_file = None
        self.drsDbConfig = None

    def __str__(self):
        return f"DeepArchiveArgs: {self.__dict__}"


class DeepArchiveParser(DbAppParser):
    # noinspection PyTypeChecker
    def __init__(self, description: str, usage: str, log_root: str = os.getcwd()):
        """
        Constructor. Sets up the arguments for DeepArchive(work, path, comment)
        """
        self._da_args = None

        super().__init__(description, usage)
        self._parser.add_argument("-l", "--log-level", dest='log_level', action='store',
                                  choices=['info', 'warning', 'error', 'debug', 'critical'], default='info',
                                  help="choice values are from python logging module")
        self._parser.add_argument("--log-root", dest='log_root', help="Parent of log files", required=False,
                                  default=log_root)
        self._parser.add_argument("-i", "--input-file", help="list of data to upload", required=True)

    @property
    def parsedArgs(self) -> DeepArchiveArgs:
        """
        Readonly, calc once
        parses the classes arguments, and returns the namespace
        :return:
        """
        # Enforce once only
        if self._da_args is None:
            self._da_args = DeepArchiveArgs()
            # noinspection PyTypeChecker
            xargs = self._parser.parse_args()
            for attr, value in xargs.__dict__.items():
                setattr(self._da_args, attr, value)

        return self._da_args
