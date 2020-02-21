# -*- coding: utf-8 -*-
# * ********************************************************************* *
# *   Copyright (C) 2018 by xmz                                           *
# * ********************************************************************* *

__author__ = "Marcin Zelek (marcin.zelek@gmail.com)"
__copyright__ = "Copyright (C) xmz. All Rights Reserved."

################################################################################
# Import(s)                                                                    #
################################################################################

import datetime


################################################################################
# Class                                                                        #
################################################################################

class JscCommon:
    """
    The class for all misc tools.
    """

    @staticmethod
    def getTimestamp(time=True, seconds=False, microseconds=False, utc=False):
        """
        Get timestamp with predefined format.

        Parameters
        ----------
        time : bool
            Show time with date
        seconds : bool
            Show seconds
        microseconds : bool
            Show microseconds
        utc : bool
            Use UTC format

        Returns
        -------
        string
            Timestamp with required format.

        """

        if utc:
            todaydate = datetime.datetime.utcnow()
        else:
            todaydate = datetime.datetime.now()
        timestemp = (str("%04d" % todaydate.year) + "-" +
                     str("%02d" % todaydate.month) + "-" +
                     str("%02d" % todaydate.day))
        if time:
            timestemp += (" " +
                          str("%02d" % todaydate.hour) + ":" +
                          str("%02d" % todaydate.minute))
            if seconds:
                timestemp += ("." + str("%02d" % todaydate.second))
                if microseconds:
                    timestemp += ("." + str("%06d" % todaydate.microsecond))
        return timestemp

################################################################################
#                                End of file                                   #
################################################################################
