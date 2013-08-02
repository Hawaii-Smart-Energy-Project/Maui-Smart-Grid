#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'

import unittest
from msg_noaa_weather_data_util import MSGWeatherDataUtil
from msg_logger import MSGLogger
from msg_db_connector import MSGDBConnector
import re
from msg_logger import MSGLogger
from msg_config import MSGConfiger


class WeatherDataLoadingTester(unittest.TestCase):
    def setUp(self):
        self.weatherUtil = MSGWeatherDataUtil()
        self.logger = MSGLogger(__name__, 'DEBUG')
        self.dbConnector = MSGDBConnector()
        self.cursor = self.dbConnector.conn.cursor()
        self.configer = MSGConfiger()


    def testLoadDataSinceLastLoaded(self):
        """
        Data should be loaded since the last data present in the database.
        """
        pass


    def testRetrieveDataSinceLastLoaded(self):
        """
        Data since the last loaded date is retrieved.
        """
        pass


    def testGetLastLoadedDate(self):
        myDate = self.weatherUtil.getLastDateLoaded(self.cursor).strftime(
            "%Y-%m-%d %H:%M:%S")
        pattern = '^(\d+-\d+-\d+\s\d+:\d+:\d+)$'
        match = re.match(pattern, myDate)
        assert match and (match.group(1) == myDate), "Date format is valid."


    def testWeatherDataPattern(self):
        myPattern = self.configer.configOptionValue('Weather Data',
                                                    'weather_data_pattern')
        testString = """<A HREF="someURL">QCLCD201208.zip</A>"""

        match = re.match(myPattern, testString)
        self.logger.log("pattern = %s" % myPattern, 'info')
        if match:
            self.logger.log("match = %s" % match)
            self.logger.log("match group = %s" % match.group(1))
        else:
            self.logger.log("match not found")
        assert match and match.group(
            1) == 'QCLCD201208.zip', "Download filename was matched."


    def testWeatherDataURL(self):
        myURL = self.configer.configOptionValue('Weather Data',
                                                'weather_data_url')
        pass


if __name__ == '__main__':
    unittest.main()
