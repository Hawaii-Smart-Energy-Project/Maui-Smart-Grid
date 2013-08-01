#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'

import unittest
from msg_noaa_weather_data_util import MSGWeatherDataUtil
from msg_logger import MSGLogger
from msg_db_connector import MSGDBConnector
import re
from msg_logger import MSGLogger


class WeatherDataLoadingTester(unittest.TestCase):
    def setUp(self):
        self.weatherUtil = MSGWeatherDataUtil()
        self.logger = MSGLogger(__name__, 'DEBUG')
        self.dbConnector = MSGDBConnector()
        self.cursor = self.dbConnector.conn.cursor()


    def testLoadDataSinceLastLoaded(self):
        """
        Data should be loaded since the last data present in the database.
        """
        pass


    def testGetLastLoadedDate(self):
        myDate = self.weatherUtil.getLastDateLoaded(self.cursor).strftime(
            "%Y-%m-%d %H:%M:%S")
        pattern = '^(\d+-\d+-\d+\s\d+:\d+:\d+)$'
        match = re.match(pattern, myDate)
        assert match and (match.group(1) == myDate), "Date format is valid."

if __name__ == '__main__':
    unittest.main()
