# -*- coding: utf-8 -*-
# * ********************************************************************* *
# *   Copyright (C) 2020 by xmz                                           *
# * ********************************************************************* *

"""
JSON Simple Config Tests - JSC Config file
"""

__author__ = "Marcin Zelek (marcin.zelek@gmail.com)"
__copyright__ = "Copyright (C) xmz. All Rights Reserved."

################################################################################
# Import(s)                                                                    #
################################################################################

import os
import shutil
import tempfile
import unittest

import jsonsimpleconfig


################################################################################
# Class                                                                        #
################################################################################

class JscConfigTest(jsonsimpleconfig.JscConfig):
    """JSC test config file."""

    config_test_dir = os.path.join(tempfile.gettempdir(), "jsc_config_test")
    _jsc_configs = [os.path.join(config_test_dir, "test_file_1.jsc"),
                    os.path.join(config_test_dir, "test_file_2.jsc"),
                    os.path.join(config_test_dir, "test_file_3.jsc")]

    @staticmethod
    def get():
        return JscConfigTest()


class JscConfigTestSuite(unittest.TestCase):
    """JSC config file test cases."""

    def setUp(self):
        """Create a temporary directory"""
        self.config_test_dir = JscConfigTest.config_test_dir
        if not (os.path.isdir(self.config_test_dir) and
                os.access(self.config_test_dir, os.W_OK)):
            os.mkdir(self.config_test_dir, 0o700)

    def tearDown(self):
        """Remove the directory after the test"""
        if os.path.isdir(self.config_test_dir):
            shutil.rmtree(self.config_test_dir)

    def test_loading_config_cascade(self):
        """Load config file cascade one by one."""
        JscConfigTest.delete()
        self.__execute_test_on_jsc_config_cascade()

    def test_loading_config(self):
        """Load config file."""
        JscConfigTest.delete()
        self.__execute_test_on_jsc_config()

    def __execute_test_file_id(self, file_id, add_section=False):
        """Load JSC from file."""

        jsc_file_body = '"variable_root":"value_root_{}"'.format(file_id)
        if add_section:
            jsc_file_body += '\n' \
                             '[Section]\n' \
                             '"file_{0}":"value_{0}"'.format(file_id)
        in_file_path = os.path.join(self.config_test_dir, "test_file_{}.jsc".format(file_id))
        with open(in_file_path, 'w') as in_file_w:
            in_file_w.write(jsc_file_body)
            in_file_w.close()

    def __execute_test_on_jsc_config_cascade(self):
        """Load JSC from file."""

        self.__execute_test_file_id(1)

        self.assertEqual("value_root_1",
                         JscConfigTest.get().get_value(None, 'variable_root', 'default'))

        self.__execute_test_file_id(2, True)

        self.assertEqual("value_root_1",
                         JscConfigTest.get().get_value(
                             None, 'variable_root', 'default'))
        self.assertIsNone(JscConfigTest.get().get_value(
            'Section', 'file_2'))
        JscConfigTest.get().init()
        self.assertEqual("value_root_2",
                         JscConfigTest.get().get_value(
                             None, 'variable_root', 'default'))
        self.assertEqual("value_2",
                         JscConfigTest.get().get_value(
                             'Section', 'file_2', 'default'))

        self.__execute_test_file_id(3, True)

        self.assertEqual("value_root_2",
                         JscConfigTest.get().get_value(
                             None, 'variable_root', 'default'))
        JscConfigTest.get().init()
        self.assertEqual("value_root_3",
                         JscConfigTest.get().get_value(
                             None, 'variable_root', 'default'))
        self.assertEqual("value_2",
                         JscConfigTest.get().get_value(
                             'Section', 'file_2', 'default'))
        self.assertEqual("value_3",
                         JscConfigTest.get().get_value(
                             'Section', 'file_3', 'default'))

    def __execute_test_on_jsc_config(self):
        """Load JSC from file."""

        self.__execute_test_file_id(1)
        self.__execute_test_file_id(2, True)
        self.__execute_test_file_id(3, True)

        self.assertEqual("value_root_3",
                         JscConfigTest.get().get_value(
                             None, 'variable_root', 'default'))
        self.assertEqual("value_2",
                         JscConfigTest.get().get_value(
                             'Section', 'file_2', 'default'))
        self.assertEqual("value_3",
                         JscConfigTest.get().get_value(
                             'Section', 'file_3', 'default'))
        self.assertEqual({'file_2': 'value_2', 'file_3': 'value_3'},
                         JscConfigTest.get().get_section('Section'))


# Execute main function
if __name__ == '__main__':
    unittest.main()

################################################################################
#                                End of file                                   #
################################################################################
