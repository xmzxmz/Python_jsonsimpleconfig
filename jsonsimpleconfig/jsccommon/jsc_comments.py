# -*- coding: utf-8 -*-
# * ********************************************************************* *
# *   Copyright (C) 2018 by xmz                                           *
# * ********************************************************************* *

__author__ = "Marcin Zelek (marcin.zelek@gmail.com)"
__copyright__ = "Copyright (C) xmz. All Rights Reserved."

###############################################################################
# Import(s)                                                                   #
###############################################################################

import os
import re


###############################################################################
# Class                                                                       #
###############################################################################


class JscComments:
    """
    The class to allow strip out comments support by JSC files.
    """

    @staticmethod
    def strip_comments(text):
        """
        Strip out comments from JSC text.

        Parameters
        ----------
        text : string
            JSC string value

        Returns
        -------
        string
            JSC value without comments

        """

        def replacer(match):
            start_group = match.group(0)
            if start_group.startswith(";") or start_group.startswith("#") or start_group.startswith("/"):
                return " "
            return start_group

        pattern = re.compile(
            r'#.*?$|;.*?$|//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"', re.DOTALL | re.MULTILINE
        )

        replaced = re.sub(pattern, replacer, text)

        return os.linesep.join([s for s in replaced.splitlines() if s.strip()])

    @staticmethod
    def strip_comments_file(in_file_path, out_file_path):
        """
        Strip out comments from JSC file and store into output file.

        Parameters
        ----------
        in_file_path : string
            JSC input file path
        out_file_path : string
            JSC output file path

        """
        with open(in_file_path, "r", encoding="UTF-8") as in_file:
            with open(out_file_path, "w", encoding="UTF-8") as out_file:
                out_file.write(JscComments.strip_comments(in_file.read()))


###############################################################################
#                                End of file                                  #
###############################################################################
