#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'
__copyright__ = 'Copyright (c) 2014, University of Hawaii Smart Energy Project'
__license__ = 'https://raw.github' \
              '.com/Hawaii-Smart-Energy-Project/Maui-Smart-Grid/master/BSD' \
              '-LICENSE.txt'

from sek.logger import SEKLogger
from msg_db_connector import MSGDBConnector
from msg_db_util import MSGDBUtil
import calendar


YEARS = [2012, 2013, 2014]


class MSGDataVerifier(object):
    """
    Perform verification procedures related to data integrity.
    """

    def __init__(self):
        """
        Constructor.
        """

        self.logger = SEKLogger(__name__, 'DEBUG')
        self.cursor = MSGDBConnector().connectDB().cursor()
        self.dbUtil = MSGDBUtil()

    def mecoReadingsDupeCount(self):
        """
        Generate counts of MECO dupe readings.
        """

        dupes = 0
        startDate = lambda y, m: '%d-%02d-%02d' % (y, m, 1)
        endDate = lambda y, m: '%d-%02d-%02d' % (
            y, m, calendar.monthrange(y, m)[1])

        for y in YEARS:
            startDates = [startDate(y, m) for m in
                          map(lambda x: x + 1, range(12))]
            endDates = [endDate(y, m) for m in map(lambda x: x + 1, range(12))]

            for start in startDates:
                cnt = self.__mecoReadingsDupeCount(start, endDates[
                    startDates.index(start)])
                self.logger.log('start: %s, dupe cnt: %s' % (start, cnt),
                                'INFO')
                dupes += cnt

        return dupes


    def __mecoReadingsDupeCount(self, startDate, endDate):
        """

        :param startDate:
        :param endDate:
        :returns: DB row count.
        """

        self.dbUtil.executeSQL(self.cursor, """SELECT "Interval".end_time,
                            "MeterData".meter_name,
                            "Reading".channel
                     FROM "MeterData"
                     INNER JOIN "IntervalReadData" ON "MeterData"
                     .meter_data_id = "IntervalReadData".meter_data_id
                     INNER JOIN "Interval" ON "IntervalReadData"
                     .interval_read_data_id = "Interval".interval_read_data_id
                     INNER JOIN "Reading" ON "Interval".interval_id = "Reading"
                     .interval_id
                     WHERE "Interval".end_time BETWEEN '%s' and '%s'
                     GROUP BY "MeterData".meter_name,
                     "Interval".end_time,
                     "Reading".channel
                     HAVING (COUNT(*) > 1)""" % (startDate, endDate))
        return len(self.cursor.fetchall())


    def egaugeAggregationCount(self):
        """
        There should not be more than 96 15-min interval endpoints within a
        single calendar day for a given sub ID.
        :return:
        """
        pass
