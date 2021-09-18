#! /bin/sh
# -*- coding: utf-8 -*-
""":"
exec python3 $0 ${1+"$@"}
"""
# * ********************************************************************* *
# *   Copyright (C) 2018 by xmz                                           *
# * ********************************************************************* *

__doc__ = "Convert JSON Simple Config file to JSON"
__author__ = "Marcin Zelek (marcin.zelek@gmail.com)"
__copyright__ = "Copyright (C) xmz. All Rights Reserved."

###############################################################################
# Import(s)                                                                   #
###############################################################################

import argparse
import logging
import signal
import sys

from jsonsimpleconfig import Jsc2JsonHelper

###############################################################################
# Module Variable(s)                                                          #
###############################################################################

VERSION_STRING = "0.0.6"
APPLICATION_NAME_STRING = "JSC converter to JSON"


###############################################################################
# Module                                                                      #
###############################################################################


def parameters():
    """
    parameters
    :return:
    """
    parser = argparse.ArgumentParser(description=APPLICATION_NAME_STRING)
    parser.add_argument("-v", "--version", action="version", version=APPLICATION_NAME_STRING + " - " + VERSION_STRING)
    parser.add_argument("-i", "--in", type=argparse.FileType("r"), help="Input file path (JSC file)", required=True)
    parser.add_argument("-o", "--out", type=argparse.FileType("w"), help="Output file path (JSON file)", required=False)
    logging_level_choices = {
        "CRITICAL": logging.CRITICAL,
        "ERROR": logging.ERROR,
        "WARNING": logging.WARNING,
        "INFO": logging.INFO,
        "DEBUG": logging.DEBUG,
    }
    parser.add_argument(
        "-ll",
        "--logging_level",
        dest="loggingLevel",
        choices=logging_level_choices.keys(),
        help="Output log level",
        required=False,
    )
    args, _ = parser.parse_known_args()

    if vars(args)["loggingLevel"] is None:
        level = logging.CRITICAL
    else:
        level = logging_level_choices.get(vars(args)["loggingLevel"], logging.CRITICAL)
    logging.basicConfig(
        format="[%(asctime)s][%(levelname)-8s] [%(module)-20s] - %(message)s", datefmt="%Y.%m.%d %H:%M.%S", level=level
    )

    jsc_file = (vars(args)["in"]).name

    if vars(args)["out"] is None:
        json_file = jsc_file + ".json"
    else:
        json_file = (vars(args)["out"]).name

    return {"loggingLevel": (vars(args)["loggingLevel"]), "json_file": json_file, "jsc_file": jsc_file}


def main(argv=sys.argv):
    """
    main
    :param argv:
    """
    signal.signal(signal.SIGINT, handler)
    args = parameters()

    if "loggingLevel" in args and args["loggingLevel"] == "DEBUG":
        Jsc2JsonHelper.convert(args["jsc_file"], args["json_file"])
    else:
        try:
            Jsc2JsonHelper.convert(args["jsc_file"], args["json_file"])
        except Exception as exception:
            print("Error!")
            logging.debug(exception)


def handler(signum, frame):
    """
    handler
    :param signum:
    :param frame:
    """
    sys.exit()


# Execute main function
if __name__ == "__main__":
    main()
    sys.exit()

###############################################################################
#                                End of file                                  #
###############################################################################
