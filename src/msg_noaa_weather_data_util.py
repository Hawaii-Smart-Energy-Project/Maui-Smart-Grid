#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'

import urllib2
import re
from msg_db_util import MSGDBUtil
from msg_logger import MSGLogger
from msg_config import MSGConfiger
import datetime as dt
from dateutil.relativedelta import relativedelta
# from msg_db_connector import MSGDBConnector

class MSGWeatherDataUtil(object):
    """
    Utility methods for working with weather data.
    """

    def __init__(self):
        """
        Constructor.

        A database connection is not maintained here to keep this class
        lightweight.
        """

        self.logger = MSGLogger(__name__, 'info')
        self.configer = MSGConfiger()
        self.url = self.configer.configOptionValue('Weather Data',
                                                   'weather_data_url')
        self.pattern = self.configer.configOptionValue('Weather Data',
                                                       'weather_data_pattern')
        self.fileList = []
        self.dateList = []
        self.fillFileListAndDateList()
        self.dbUtil = MSGDBUtil()
        # self.dbConnector = MSGDBConnector()
        # self.cursor = self.dbConnector.conn.cursor()
        # self.lastLoadedDate = self.getLastDateLoaded(self.cursor)


    def fillFileListAndDateList(self):
        """
        Return a list of weather files used in processing weather data.
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

        sql = """select wban, datetime, record_type from "WeatherNOAA"
                 ORDER BY datetime desc limit 1"""

        self.dbUtil.executeSQL(cursor, sql)
        row = cursor.fetchone()
        # self.logger.log('Date last loaded = %s' % row[1], 'info')
        return row[1]


    def getKeepList(self, fileList, cursor):
        """
        The Keep List is the list of filenames of containing data that are
        within the
        month of the last loaded date or are beyond the last loaded date.

        :param: fileList: A list of files containing weather data.
        :param: DB cursor.
        :returns: List of weather data filenames to process.
        """

        keepList = []
        i = 0
        for date in fileList:
            listDate = dt.datetime.strptime(self.datePart(filename = date),
                                            "%Y%m")
            # print listDate
            lastDate = self.getLastDateLoaded(cursor)
            if lastDate < listDate:
                keepList.append((i, listDate))
            i += 1

        if keepList:
            keepList.sort()
            # print "New data exists."

            # Also retrieve one month less than the earliest date in the keep
            #  list.
            keepList.append(
                (
                    keepList[0][0] - 1,
                    keepList[0][1] - relativedelta(months = 1)))

            # print "keepList:"
            # print keepList

            # Rewrite keep list.
            fileListFollowUp = []
            for d in keepList:
                fileListFollowUp.append(fileList[d[0]])

            # print "File List Follow Up:"
            # print fileListFollowUp

        return fileListFollowUp

