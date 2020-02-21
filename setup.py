# -*- coding: utf-8 -*-
# * ********************************************************************* *
# *   Copyright (C) 2020 by xmz                                           *
# * ********************************************************************* *

__doc__ = "JSON Simple Config Setup"
__author__ = "Marcin Zelek"
__email__ = "marcin.zelek@gmail.com"
__copyright__ = "Copyright (C) xmz. All Rights Reserved."
__license__ = "MIT"
__version__ = "0.2"

################################################################################
# Import(s)                                                                    #
################################################################################

import os

from setuptools import setup

################################################################################
# Module                                                                       #
################################################################################

description = 'The simple idea to prepare configuration for your application.'


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


try:
    long_description = read('README.rst')
except IOError:
    long_description = description

setup(
    name='jsonsimpleconfig',
    version=__version__,
    description=description,
    long_description=long_description,
    keywords="json configuration jsc simple config",
    author=__author__,
    author_email=__email__,
    license=__license__,
    url='https://github.com/xmzxmz/jsonsimpleconfig',
    package_data={'': ['jscresources/*.template']},
    include_package_data=True,
    packages=['jsonsimpleconfig',
              'jsonsimpleconfig.jsccommon',
              'jsonsimpleconfig.jscdata',
              'jsonsimpleconfig.jscextractor',
              'jsonsimpleconfig.jschelper',
              'jsonsimpleconfig.jscparser'],
    entry_points=
    {
        'console_scripts':
            [
                'json2jsc = jsonsimpleconfig.json2jsc:main',
                'jsc2json = jsonsimpleconfig.jsc2json:main',
                'jscValue = jsonsimpleconfig.jscValue:main',
                'jscPrint = jsonsimpleconfig.jscPrint:main',
            ],
    },
    zip_safe=False
)

################################################################################
#                                End of file                                   #
################################################################################
