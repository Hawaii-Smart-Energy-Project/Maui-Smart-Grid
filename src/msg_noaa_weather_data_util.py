#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'

import urllib2
import re
from msg_db_util import MSGDBUtil
from msg_logger import MSGLogger
from msg_config import MSGConfiger


class MSGWeatherDataUtil(object):
    """
    Utility methods for working with weather data.
    """

    def __init__(self):
        """
        Constructor.
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

    def fillFileListAndDateList(self):
        """
        Return a list of weather files used in processing weather data.
        """

        response = urllib2.urlopen(self.url).read()

        for filename in re.findall(self.pattern, response):
            self.fileList.append(filename[0])
            self.dateList.append(self.datePart(filename[0]))


    def datePart(self, filename):
        """
        Return the date part of a NOAA weather data filename.
        :param: The filename.
        :returns: The date part of the filename.
        """
        newName = filename.replace("QCLCD", '')
        newName = newName.replace(".zip", '')
        return newName

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