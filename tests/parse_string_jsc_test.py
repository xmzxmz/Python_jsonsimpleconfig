# -*- coding: utf-8 -*-
# * ********************************************************************* *
# *   Copyright (C) 2020 by xmz                                           *
# * ********************************************************************* *

"""
JSON Simple Config Tests - Parsing
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

class StringJscTestSuite(unittest.TestCase):
    """String base JSC test cases."""

    __example_jsc = '"variable_root":"value_root"'

    def test_load_empty(self):
        """Loads empty string."""
        self.assertIsNone(jsonsimpleconfig.loads(""))

    def test_load_example_jsc(self):
        """Loads example JSC string."""
        self.assertIsNotNone(jsonsimpleconfig.loads(StringJscTestSuite.__example_jsc))
        self.assertIsInstance(jsonsimpleconfig.loads(StringJscTestSuite.__example_jsc),
                              jsonsimpleconfig.JscData)


# Execute main function
if __name__ == '__main__':
    unittest.main()

################################################################################
#                                End of file                                   #
################################################################################
