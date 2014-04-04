#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'
__copyright__ = 'Copyright (c) 2013, University of Hawaii Smart Energy Project'
__license__ = 'https://raw.github' \
              '.com/Hawaii-Smart-Energy-Project/Maui-Smart-Grid/master/BSD' \
              '-LICENSE.txt'

from datetime import datetime as dt
from msg_logger import MSGLogger
from dateutil import rrule
import calendar


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
            self.logger.log('Processing day %s.' % day)
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

        return dt.now().strftime('%Y-%m-%d_%H%M%S')


    def splitStringDates(self, startDate = '', endDate = ''):
        """
        Break down two dates into a list containing the start and end dates
        for each month within the range.

        :param startDate: string
        :param endDate: string
        :return: List of tuples.
        """

        # self.logger.log('start,end: %s,%s' % (startDate, endDate))

        myDatetime = lambda x: dt.strptime(x, '%Y-%m-%d')
        firstDay = lambda x: dt.strptime(x.strftime('%Y-%m-01'), '%Y-%m-%d')
        startDates = map(firstDay, list(
            rrule.rrule(rrule.MONTHLY, dtstart = myDatetime(startDate),
                        until = myDatetime(endDate))))
        startDates[0] = myDatetime(startDate)
        lastDay = lambda x: dt.strptime('%d-%d-%d' % (
            x.year, x.month, calendar.monthrange(x.year, x.month)[1]),
                                        '%Y-%m-%d')
        endDates = map(lastDay, startDates)
        endDates[-1] = myDatetime(endDate)
        assert len(startDates) == len(
            endDates), 'Mismatch of start and end dates.'
        return zip(startDates, endDates)


    def splitDates(self, start = None, end = None):
        """
        Break down two dates into a list containing the start and end dates
        for each month within the range.

        :param start: datetime
        :param end: datetime
        :return: List of tuples.
        """

        self.logger.log('start {}, end {}'.format(start, end), 'debug')

        # First day of the month.

        # @TO BE REVIEWED
        # Observed at least one case where firstDay was not correct for a
        # time range. The first day was listed as 2014-03-01 and the last day
        # came out as 2014-04-04 for that month. 2014-04-01 was NOT INCLUDED.
        #
        # The range was:
        # start: (datetime.datetime(2013, 8, 21, 15, 0)
        # end: datetime.datetime(2014, 4, 4, 0, 4)
        #
        # The overall effect on processing is negligible because the end date
        # still gets set correctly but it should be determined why there is a
        # discrepancy.

        firstDay = lambda x: dt.strptime(x.strftime('%Y-%m-01'), '%Y-%m-%d')
        startDates = map(firstDay, list(
            rrule.rrule(rrule.MONTHLY, dtstart = start, until = end)))
        startDates[0] = start

        lastDay = lambda x: dt.strptime('%d-%d-%d' % (
            x.year, x.month, calendar.monthrange(x.year, x.month)[1]),
                                        '%Y-%m-%d')
        endDates = map(lastDay, startDates)
        self.logger.log('start dates {}'.format(startDates), 'debug')
        self.logger.log('end dates {}'.format(endDates), 'debug')
        endDates[-1] = end

        assert len(startDates) == len(
            endDates), 'Mismatch of start and end dates.'
        return zip(startDates, endDates)

# For debugging:
# timeUtil = MSGTimeUtil()

# testDays = set()
# testDays.add(dt.datetime.strptime("2003-01-01 00:00", "%Y-%m-%d %H:%M"))
# testDays.add(dt.datetime.strptime("2003-01-02 00:00", "%Y-%m-%d %H:%M"))
# testDays.add(dt.datetime.strptime("2003-01-01 00:00", "%Y-%m-%d %H:%M"))

# print timeUtil.reportOfDays(testDays)
