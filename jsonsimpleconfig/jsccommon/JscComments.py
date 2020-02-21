# -*- coding: utf-8 -*-
# * ********************************************************************* *
# *   Copyright (C) 2018 by xmz                                           *
# * ********************************************************************* *

__author__ = "Marcin Zelek (marcin.zelek@gmail.com)"
__copyright__ = "Copyright (C) xmz. All Rights Reserved."

################################################################################
# Import(s)                                                                    #
################################################################################

import os
import re


################################################################################
# Class                                                                        #
################################################################################

class JscComments:
    """
    The class to allow strip out comments support by JSC files.
    """

    @staticmethod
    def stripComments(text):
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
            startGroup = match.group(0)
            if startGroup.startswith(';') or \
                    startGroup.startswith('#') or \
                    startGroup.startswith('/'):
                return " "
            else:
                return startGroup

        pattern = re.compile(
            r'#.*?$|;.*?$|//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
            re.DOTALL | re.MULTILINE
        )

        replaced = re.sub(pattern, replacer, text)

        return os.linesep.join([s for s in replaced.splitlines() if s.strip()])

    @staticmethod
    def stripCommentsFile(inFilePath, outFilePath):
        """
        Strip out comments from JSC file and store into output file.

        Parameters
        ----------
        inFilePath : string
            JSC input file path
        outFilePath : string
            JSC output file path

        """
        inFile = open(inFilePath)
        if inFile:
            if inFile.readable():
                outFile = open(outFilePath, 'w', encoding='utf-8')
                if outFile:
                    if outFile.writable():
                        outFile.write(JscComments.stripComments(inFile.read()))
                    outFile.close()
            inFile.close()

################################################################################
#                                End of file                                   #
################################################################################
