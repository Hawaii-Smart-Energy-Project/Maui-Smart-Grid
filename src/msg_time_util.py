#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'
__copyright__ = 'Copyright (c) 2013, University of Hawaii Smart Energy Project'
__license__ = 'https://raw.github' \
              '.com/Hawaii-Smart-Energy-Project/Maui-Smart-Grid/master/BSD' \
              '-LICENSE.txt'

from time import strptime
from datetime import datetime as dt
import sys
from msg_logger import MSGLogger


class MSGTimeUtil(object):
    """
    Utilities for working with time.
    """

    def __init__(self):
        """
        Constructor.
        """

        self.logger = MSGLogger(__name__, 'debug')

    def reportOfDays(self, datetimes = None):
        """
        Return report of days processed given a set of days.

        :param datetimes: A set of datetimes.
        :returns: Report of processing as a string.
        """

        #  @todo Verify datetimes is a Set.

        # self.logger.log("datetimes = %s" % datetimes, 'debug')

        if datetimes is None:
            return "No days processed."

        myDates = set()
        for day in datetimes:
            assert type(day) is dt.datetime, "Day should be type datetime."
            myDates.add(day.date())

        datetimeList = list(myDates)
        datetimeList.sort()

        countOfDays = len(datetimeList)
        firstDay = datetimeList[0]
        lastDay = datetimeList[len(datetimeList) - 1]

        if countOfDays == 1:
            return "Processed 1 day with date %s." % (firstDay)
        else:
            return "Processed %s days between %s to %s, inclusive." % (
                countOfDays, firstDay, lastDay)

    def conciseNow(self):
        """
        Returns the current date and time in a concise format.
        """

        return dt.strftime(dt.now(), '%Y-%m-%d_%H%m%S')



# For debugging
# timeUtil = MSGTimeUtil()

# testDays = set()
# testDays.add(dt.datetime.strptime("2003-01-01 00:00", "%Y-%m-%d %H:%M"))
# testDays.add(dt.datetime.strptime("2003-01-02 00:00", "%Y-%m-%d %H:%M"))
# testDays.add(dt.datetime.strptime("2003-01-01 00:00", "%Y-%m-%d %H:%M"))

# print timeUtil.reportOfDays(testDays)
