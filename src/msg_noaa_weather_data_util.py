#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'
__copyright__ = 'Copyright (c) 2013, University of Hawaii Smart Energy Project'
__license__ = 'https://raw.github' \
              '.com/Hawaii-Smart-Energy-Project/Maui-Smart-Grid/master/BSD' \
              '-LICENSE.txt'

import urllib2
import re
from msg_db_util import MSGDBUtil
from msg_logger import MSGLogger
from msg_configer import MSGConfiger
import datetime as dt
from dateutil.relativedelta import relativedelta
import calendar


WEATHER_DATA_TABLE = "WeatherNOAA"


class MSGWeatherDataUtil(object):
    """
    Utility methods for working with weather data.
    """

    def __init__(self):
        """
        Constructor.

        A database connection is not maintained here to keep this class
        lightweight. This results in the class not having a parameter for
        TESTING MODE.
        """

        self.logger = MSGLogger(__name__, 'info')
        self.configer = MSGConfiger()
        self.url = self.configer.configOptionValue('Weather Data',
                                                   'weather_data_url')
        self.pattern = self.configer.configOptionValue('Weather Data',
                                                       'weather_data_pattern')
        self.fileList = []
        self.dateList = [] # List of dates corresponding weather data files.
        self.fillFileListAndDateList()
        self.dbUtil = MSGDBUtil()


    def fillFileListAndDateList(self):
        """
        Return a list of weather files obtained from the remote server used in processing weather data.
        """

        response = urllib2.urlopen(self.url).read()

        for filename in re.findall(self.pattern, response):
            self.fileList.append(filename[0])
            self.dateList.append(self.datePart(filename = filename[0]))


    def datePart(self, filename = None, datetime = None):
        """
        Return the date part of a NOAA weather data filename.

        :param: The filename.
        :param: A datetime object.
        :returns: The date part of the given parameter.
        """

        assert filename == None or datetime == None, "One argument is allowed."
        if filename:
            newName = filename.replace("QCLCD", '')
            newName = newName.replace(".zip", '')
            return newName
        if datetime:
            return datetime.strftime('%Y-%m-%d')

    def getLastDateLoaded(self, cursor):
        """
        Return the last date of loaded weather data.

        :returns: Last date.
        """

        sql = """select wban, datetime, record_type from "%s"
                 ORDER BY datetime desc limit 1""" % WEATHER_DATA_TABLE

        self.dbUtil.executeSQL(cursor, sql)
        row = cursor.fetchone()
        # self.logger.log('Date last loaded = %s' % row[1], 'info')
        return row[1]


    def getKeepList(self, fileList, cursor):
        """
        The Keep List is the list of filenames of files containing data that are
        within the month of the last loaded date or are beyond the last loaded
        date.

        :param: fileList: A list of files containing weather data.
        :param: DB cursor.
        :returns: List of weather data filenames to process.
        """

        keepList = []
        i = 0
        for date in fileList:
            self.logger.log('Examining date %s.' % date)

            # The list date should be the last day of the month.

            listDate = dt.datetime.strptime(self.datePart(filename = date),
                                            "%Y%m")
            lastDay = calendar.monthrange(listDate.year, listDate.month)[1]
            listDate = dt.datetime.strptime(
                '%s-%s-%s' % (listDate.year, listDate.month, lastDay),
                "%Y-%m-%d")
            self.logger.log('List date = %s.' % listDate)
            lastDate = self.getLastDateLoaded(cursor)

            self.logger.log('last date = %s' % lastDate)

            if lastDate <= listDate:
                keepList.append((i, listDate))
            i += 1

        if keepList:
            keepList.sort()

            # Also retrieve one month less than the earliest date in the keep
            #  list.
            keepList.append(
                (
                    keepList[0][0] - 1,
                    keepList[0][1] - relativedelta(months = 1)))

        return [fileList[d[0]] for d in keepList]

