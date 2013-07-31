#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'

import unittest
from msg_weather_data_util import MSGWeatherDataUtil
from msg_logger import MSGLogger
from msg_db_connector import MSGDBConnector


class WeatherDataLoadingTester(unittest.TestCase):

    def setUp(self):
        self.weatherUtil = MSGWeatherDataUtil()
        self.logger = MSGLogger(__name__, 'DEBUG')
        self.dbConnector = MSGDBConnector()

    def testLoadDataSinceLastLoaded(self):
        """
        Data should be loaded since the last data present in the database.
        """
        pass

    def testGetLastLoadedDate(self):
        self.weatherUtil.getLastDateLoaded()
        pass


if __name__ == '__main__':
    unittest.main()
