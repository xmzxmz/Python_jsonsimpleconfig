# -*- coding: utf-8 -*-
# * ********************************************************************* *
# *   Copyright (C) 2020 by xmz                                           *
# * ********************************************************************* *

"""
JSON Simple Config Tests - JSC data operations
"""

__author__ = "Marcin Zelek (marcin.zelek@gmail.com)"
__copyright__ = "Copyright (C) xmz. All Rights Reserved."

################################################################################
# Import(s)                                                                    #
################################################################################

import unittest

import jsonsimpleconfig


################################################################################
# Class                                                                        #
################################################################################

class JscDataTestSuite(unittest.TestCase):
    """JSC data operations test cases."""

    __example_one_jsc = '"variable_root":"value_root"'
    __example_two_jsc = '"variable_root":"value_root_two"\n' \
                        '[section_two]\n' \
                        '"variable_section":"value_section"\n'

    def test_jsc_data_operations(self):
        """Loads example JSC string."""
        data_one = jsonsimpleconfig.loads(JscDataTestSuite.__example_one_jsc)
        self.assertIsNotNone(data_one)
        self.assertIsInstance(data_one, jsonsimpleconfig.JscData)
        value = data_one.getValue(None, "variable_root")
        self.assertIsNotNone(value)
        self.assertEqual(value, "value_root")
        section = data_one.getSection()
        self.assertIsNotNone(section)
        self.assertEqual(section["variable_root"], "value_root")
        data_two = jsonsimpleconfig.loads(JscDataTestSuite.__example_two_jsc)
        data_one.merge(data_two)
        value = data_one.getValue(None, "variable_root")
        self.assertEqual(value, "value_root_two")
        section = data_two.getSection("section_two")
        self.assertIsNotNone(section)
        self.assertEqual(section["variable_section"], "value_section")
        self.assertEqual(data_one.getValue("section_two", "variable_section"), "value_section")


# Execute main function
if __name__ == '__main__':
    unittest.main()

################################################################################
#                                End of file                                   #
################################################################################
