#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'

from time import strptime
import datetime as dt
import sys
from msg_logger import MSGLogger


class MSGTimeUtil(object):
    """
    """

    def __init__(self):
        """
        Constructor.
        """

        self.logger = MSGLogger(__name__, 'debug')

    def reportOfDays(self, datetimes = None):
        """
        Return report of days processed.

        :param datetimes: A set of datetimes.

        @todo Verify datetimes is a Set.
        """

        self.logger.log("datetimes = %s" % datetimes, 'debug')

        if datetimes is None:
            return "No days processed."

        myDates = set()
        for day in datetimes:
            assert type(day) is dt.datetime, "Day should be type datetime."
            myDates.add(day)

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


# For debugging
timeUtil = MSGTimeUtil()

testDays = set()
testDays.add(dt.datetime.strptime("2003-01-01 00:00", "%Y-%m-%d %H:%M"))
testDays.add(dt.datetime.strptime("2003-01-02 00:00", "%Y-%m-%d %H:%M"))
testDays.add(dt.datetime.strptime("2003-01-01 00:00", "%Y-%m-%d %H:%M"))

print timeUtil.reportOfDays(testDays)
