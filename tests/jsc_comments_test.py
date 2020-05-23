# -*- coding: utf-8 -*-
# * ********************************************************************* *
# *   Copyright (C) 2020 by xmz                                           *
# * ********************************************************************* *

"""
JSON Simple Config Tests - Comments
"""

__author__ = "Marcin Zelek (marcin.zelek@gmail.com)"
__copyright__ = "Copyright (C) xmz. All Rights Reserved."

###############################################################################
# Import(s)                                                                   #
###############################################################################

import datetime
import os
import shutil
import tempfile
import unittest

import jsonsimpleconfig


###############################################################################
# Class                                                                       #
###############################################################################

class JscCommentsTestSuite(unittest.TestCase):
    """Comments for JSC test cases."""

    __example_jsc = '"variable_root":"value_root"'

    def setUp(self):
        """Create a temporary directory"""
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Remove the directory after the test"""
        if os.path.isdir(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_remove_one_line_comment(self):
        """Remove one line comment."""
        self.assertIsNone(jsonsimpleconfig.loads("# " + JscCommentsTestSuite.__example_jsc))
        self.assertIsNone(jsonsimpleconfig.loads("// " + JscCommentsTestSuite.__example_jsc))
        self.assertIsNone(jsonsimpleconfig.loads("; " + JscCommentsTestSuite.__example_jsc))
        self.assertEqual('',
                         jsonsimpleconfig.JscComments.strip_comments(
                             "# " + JscCommentsTestSuite.__example_jsc))
        self.assertEqual('',
                         jsonsimpleconfig.JscComments.strip_comments(
                             "// " + JscCommentsTestSuite.__example_jsc))
        self.assertEqual('',
                         jsonsimpleconfig.JscComments.strip_comments(
                             "; " + JscCommentsTestSuite.__example_jsc))

    def test_remove_multi_line_comments(self):
        """Remove multi line comment."""
        self.assertIsNone(jsonsimpleconfig.loads(
            "/* " + JscCommentsTestSuite.__example_jsc + " */"))
        self.assertIsNone(jsonsimpleconfig.loads(
            "/* \n" + JscCommentsTestSuite.__example_jsc + "\n */"))
        self.assertIsInstance(jsonsimpleconfig.loads(
            "// \n" + JscCommentsTestSuite.__example_jsc + "\n //"), jsonsimpleconfig.JscData)

    def test_one_line_comment_file(self):
        """Remove one line comment from file."""
        self.assertIsNone(self.__execute_test_on_file("# " + JscCommentsTestSuite.__example_jsc))
        self.assertIsNone(self.__execute_test_on_file("// " + JscCommentsTestSuite.__example_jsc))
        self.assertIsNone(self.__execute_test_on_file("; " + JscCommentsTestSuite.__example_jsc))

        self.assertIsInstance(
            self.__execute_test_on_file(
                "# " + JscCommentsTestSuite.__example_jsc + os.linesep + JscCommentsTestSuite.__example_jsc),
            jsonsimpleconfig.JscData)

    def test_multi_line_comments_file(self):
        """Remove multi line comment from file."""
        self.assertIsNone(
            self.__execute_test_on_file(
                "/* " + JscCommentsTestSuite.__example_jsc + " */"))
        self.assertIsNone(
            self.__execute_test_on_file(
                "/* \n" + JscCommentsTestSuite.__example_jsc + "\n */"))
        self.assertIsInstance(
            self.__execute_test_on_file(
                "// \n" + JscCommentsTestSuite.__example_jsc + "\n //"),
            jsonsimpleconfig.JscData)

    def __execute_test_on_file(self, jsc_file_body):
        """Load JSC from file."""

        in_file_path = os.path.join(
            self.test_dir, str("test_file_%s.jsc" % datetime.datetime.utcnow().timestamp()))
        with open(in_file_path, 'w') as in_file_w:
            in_file_w.write(jsc_file_body)
            in_file_w.close()
            with open(in_file_path, 'r') as in_file_r:
                self.assertEqual(in_file_r.read(), jsc_file_body)
                in_file_r.close()
            return jsonsimpleconfig.load(in_file_path)
        return None


# Execute main function
if __name__ == '__main__':
    unittest.main()

###############################################################################
#                                End of file                                  #
###############################################################################
