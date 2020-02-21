# -*- coding: utf-8 -*-
# * ********************************************************************* *
# *   Copyright (C) 2018 by xmz                                           *
# * ********************************************************************* *

__author__ = "Marcin Zelek (marcin.zelek@gmail.com)"
__copyright__ = "Copyright (C) xmz. All Rights Reserved."

################################################################################
# Import(s)                                                                    #
################################################################################

import logging

from jsonsimpleconfig import JscParser, JscData, JsonExtractor


################################################################################
# Class                                                                        #
################################################################################

class Jsc2JsonHelper:

    @staticmethod
    def convert(jscFile, jsonFile):

        jscParser = JscParser()
        jscData = jscParser.parseFile(jscFile)

        if jscData is not None and isinstance(jscData, JscData):
                logging.info('JSC file is correct. Generating JSON ...')
                logging.info('JSON location: ' + jsonFile)
                jsonExtractor = JsonExtractor(jscData)
                jsonExtractor.extractToFile(jsonFile)

        else:
            logging.error('Incorrect JSC or file is empty.')

################################################################################
#                                End of file                                   #
################################################################################
