"""
Test the permutations of the source and dest
"""
import unittest
from pathlib import Path

import sys

from archive_ops.DipLog import DipLogParser


class DipLogParserTest(unittest.TestCase):
    """
    Test parsing of DipLog arguments
    """

    def test_id_and_return_parse(self):
        expect_dip_id = '12346'
        expect_dip_rc = 42
        sys.argv = ["DipLogParserTest.py", '--dip_id', expect_dip_id, '-r', str(expect_dip_rc)]
        dlp = DipLogParser("usage", "desc")
        test_ns = dlp.parsedArgs
        self.assertIsNotNone(test_ns)
        self.assertEqual(test_ns.dip_id, expect_dip_id)
        self.assertEqual(test_ns.activity_return_code, expect_dip_rc)

    def test_required_args_parse(self):
        """
        Test that the parser correctly parses when only the required args are given
           self._parser.add_argument("-a", "--activity_type", help="Destination repository",
                                  choices=['DRS', 'IA', 'BUDA', 'DEEP_ARCHIVE', 'ARCHIVE', 'SINGLE_ARCHIVE',
                                           'SINGLE_ARCHIVE_REMOVED', 'GOOGLE_BOOKS'],
                                  required=False)

        self._parser.add_argument("-w", "--work_name", help="work being distributed", required=False)
        self._parser.add_argument("-b", "--begin_time", help="time of beginning - ')" "yyyy-mm-dd hh:mm:ss bash
        format date +\'%%Y-%%m-%%d %%R:%%S\'", required=False, type=str2datetime) :return:
        """
        expect_activity_type = 'GOOGLE_BOOKS'
        expect_begin_time = '2000-01-01 12:34:56'
        expect_work_name = 'W123456'
        sys.argv = ["DipLogParserTest.py", '--activity_type', expect_activity_type, '--work_name', expect_work_name,
                    "--begin_time", expect_begin_time]
        dlp = DipLogParser("usage", "desc")
        test_ns = dlp.parsedArgs

        self.assertIsNotNone(test_ns)
        self.assertEqual(test_ns.activity_type, expect_activity_type)
        self.assertEqual(test_ns.work_name, expect_work_name)
        self.assertEqual(str(test_ns.begin_time), expect_begin_time)

    def test_reallypath_unqualified(self):
        """
        Test that reallypath fully qualifies
        :return:
        """
        # Arrange
        expect_activity_type = 'GOOGLE_BOOKS'

        expect_begin_time = '2000-01-01 12:34:56'
        expect_work_name = 'W123456'
        source_dip_root = "prepend_source"
        dest_dip_root = "prepend_dest"
        expect_dip_source = str(Path(source_dip_root).absolute().resolve())
        expect_dip_dest = str(Path(dest_dip_root).absolute().resolve())
        sys.argv = ["DipLogParserTest.py",
                    '--activity_type', expect_activity_type,
                    '--work_name', expect_work_name,
                    "--begin_time", expect_begin_time,
                    "--resolve-sym-links",
                    "prepend_source", "prepend_dest"]

        # Act
        dlp = DipLogParser("usage", "desc")

        dla = dlp.parsedArgs

        # Assert
        # should have one return
        self.assertEqual(dla.dip_source_path, expect_dip_source)
        self.assertEqual(dla.dip_dest_path, expect_dip_dest)

    def test_reallypath_preserves_URI(self):
        """
        Test that reallypath preserves URI values
        :return:
        """
        # Arrange
        expect_activity_type = 'GOOGLE_BOOKS'

        expect_begin_time = '2000-01-01 12:34:56'
        expect_work_name = 'W123456'
        source_dip_root = "s3://prepend_source"
        dest_dip_root = "ia://prepend_dest"
        expect_dip_source = source_dip_root
        expect_dip_dest = dest_dip_root
        sys.argv = ["DipLogParserTest.py", '--activity_type', expect_activity_type, '--work_name', expect_work_name,
                    "--begin_time", expect_begin_time, source_dip_root, dest_dip_root]

        # Act
        dlp = DipLogParser("usage", "desc")

        dla = dlp.parsedArgs

        # Assert
        # should have one return
        self.assertEqual(dla.dip_source_path, expect_dip_source)
        self.assertEqual(dla.dip_dest_path, expect_dip_dest)

    def test_reallypath_preserves_UNC(self):
        """
        Test that reallypath preserves URI values
        :return:
        """
        # Arrange
        expect_activity_type = 'GOOGLE_BOOKS'

        expect_begin_time = '2000-01-01 12:34:56'
        expect_work_name = 'W123456'
        source_dip_root = "//frelm/prepend_source"
        dest_dip_root = "//frelm/prepend_dest"
        expect_dip_source = source_dip_root
        expect_dip_dest = dest_dip_root
        sys.argv = ["DipLogParserTest.py", '--activity_type', expect_activity_type, '--work_name', expect_work_name,
                    "--begin_time", expect_begin_time, source_dip_root, dest_dip_root]

        # Act
        dlp = DipLogParser("usage", "desc")

        dla = dlp.parsedArgs

        # Assert
        # should have one return
        self.assertEqual(dla.dip_source_path, expect_dip_source)
        self.assertEqual(dla.dip_dest_path, expect_dip_dest)

    def test_reallypath_preserves_UNC_2(self):
        """
        Test that reallypath preserves URI values
        :return:
        """
        # Arrange
        expect_activity_type = 'GOOGLE_BOOKS'

        expect_begin_time = '2000-01-01 12:34:56'
        expect_work_name = 'W123456'
        source_dip_root = "\\frelm\prepend_source"
        dest_dip_root = "\\frelm\prepend_dest"
        expect_dip_source = source_dip_root
        expect_dip_dest = dest_dip_root
        sys.argv = ["DipLogParserTest.py", '--activity_type', expect_activity_type, '--work_name', expect_work_name,
                    "--begin_time", expect_begin_time, source_dip_root, dest_dip_root]

        # Act
        dlp = DipLogParser("usage", "desc")

        dla = dlp.parsedArgs

        # Assert
        # should have one return
        self.assertEqual(dla.dip_source_path, expect_dip_source)
        self.assertEqual(dla.dip_dest_path, expect_dip_dest)

    def test_reallypath_no_middle_UNC(self):
        """
        Test that reallypath preserves URI values
        :return:
        """
        # Arrange
        expect_activity_type = 'GOOGLE_BOOKS'

        expect_begin_time = '2000-01-01 12:34:56'
        expect_work_name = 'W123456'
        source_dip_root = "blarg\\frelm\prepend_source"
        dest_dip_root = "blarg\\frelm\prepend_dest"

        expect_dip_source = str(Path(source_dip_root).absolute().resolve())
        expect_dip_dest = str(Path(dest_dip_root).absolute().resolve())
        sys.argv = ["DipLogParserTest.py",
                    '--activity_type', expect_activity_type,
                    '--work_name', expect_work_name,
                    "--begin_time", expect_begin_time,
                    "--resolve-sym-links",
                    source_dip_root,
                    dest_dip_root]

        # Act
        dlp = DipLogParser("usage", "desc")

        dla = dlp.parsedArgs

        # Assert
        # should have one return
        self.assertEqual(dla.dip_source_path, expect_dip_source)
        self.assertEqual(dla.dip_dest_path, expect_dip_dest)

    def test_alt_db_no_exists(self):
        """
        Test that reallypath preserves URI values
        :return:
        """
        real_config: str = "~/.config/bdrc/db_unit_test.config"
        not_exists_config: str = "doesnt exist"
        test_cases = [
            (f"no_section:{real_config}", "QA_TEST_ACTIVITY", KeyError, False),  # should raise KeyError
            (f"no_section:{not_exists_config}", "QA_TEST_ACTIVITY", SystemExit, False),
            # should raise FileNotFoundError
            (f"qa:{real_config}", "QA_TEST_ACTIVITY", None, True)
        ]
        for test_db_config, activity, exception, expected in test_cases:
            with self.subTest(tdb=test_db_config, a=activity, ex=exception, v=expected):
                rv: () = self.db_config_scenario(db_config=test_db_config, activity=activity)
                ae: Exception = rv[0]
                av: bool = rv[1]

                if ae is None:

                    # If the section or file is there, then test the returned activity
                    self.assertEqual(av, expected)
                else:

                    # If the section or file is not there, then there should be an exception
                    self.assertIsInstance(ae, exception)

    def db_config_scenario(self, db_config: str, activity: str) -> ():
        """
        test a specific db scenario, return the vector of exception and truth
        :return:

        """
        # Arrange
        sys.argv = ["DipLogParserTest.py",
                    '--activity_type', activity,
                    '--dip_id', '0xbadfood',  # generic hex value
                    "--drsDbConfig", db_config
                    ]
        # returned Exception
        re: Exception = None
        # returned if there was no exception
        rb: bool = False

        # Act
        from argparse import ArgumentTypeError
        try:
            dlp = DipLogParser("usage", "desc")
        except (KeyError, ArgumentTypeError) as e:
            re = e
        except SystemExit as se:
            re = se


        if re is None:
            # Test actual working value
            # this is, to some extent, testing the database, but ONLY the tested db has this value in
            # its acitivities table
            dla = dlp.parsedArgs
            rb = activity.upper() == dla.activity_type.upper()

        return re, rb


if __name__ == '__main__':
    unittest.main()
