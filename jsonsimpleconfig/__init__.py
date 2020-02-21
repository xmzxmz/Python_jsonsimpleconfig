"""
JSON Simple Config

The simple idea to prepare and manage configuration for your application.
"""

# * ********************************************************************* *
# *   Copyright (C) 2020 by xmz                                           *
# * ********************************************************************* *

################################################################################
# Import(s)                                                                    #
################################################################################

from .jsccommon import JscComments, JscCommon
from .jscdata import JscData, JscSection
from .jscparser import Json, JscParser
from .jscextractor import JscExtractor, JscHeader, JsonExtractor
from .jschelper import Jsc, Json2JscHelper, Jsc2JsonHelper, JscConfig


################################################################################
# Module                                                                       #
################################################################################

def load(jscFile, refresh=False):
    return Jsc.get(jscFile, refresh)


def loads(jscString):
    return Jsc.gets(jscString)


__all__ = ('JscCommon',
           'JscComments',
           'Json2JscHelper',
           'Jsc2JsonHelper',
           'Json',
           'JscParser',
           'JscData',
           'JscSection',
           'JscExtractor',
           'JsonExtractor',
           'JscHeader',
           'Jsc',
           'JscConfig')

################################################################################
#                                End of file                                   #
################################################################################
