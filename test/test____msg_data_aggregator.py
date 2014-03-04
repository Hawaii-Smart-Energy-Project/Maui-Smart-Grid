#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'
__copyright__ = 'Copyright (c) 2014, University of Hawaii Smart Energy Project'
__license__ = 'https://raw.github' \
              '.com/Hawaii-Smart-Energy-Project/Maui-Smart-Grid/master/BSD' \
              '-LICENSE.txt'

import unittest
from msg_logger import MSGLogger
from msg_data_aggregator import MSGDataAggregator


class MSGDataAggregatorTester(unittest.TestCase):
    """
    Unit tests for MSG Data Aggregator.
    """

    def setUp(self):
        """
        Constructor.
        """
        self.logger = MSGLogger(__name__, 'DEBUG')
        self.aggregator = MSGDataAggregator()
        self.testStart = '2014-01-02 12:00'
        self.testEnd = '2014-01-02 13:00'

    def testIrradianceFetch(self):
        """
        """
        rows = []
        for row in self.aggregator._MSGDataAggregator__rawIrradianceData(
                startDate = self.testStart, endDate = self.testEnd):
            rows.append(row)
        self.assertIsNotNone(rows, 'Rows are present.')

    def testWeatherFetch(self):
        """
        """
        rows = []
        for row in self.aggregator._MSGDataAggregator__rawWeatherData(
                startDate = self.testStart, endDate = self.testEnd):
            rows.append(row)
        self.assertIsNotNone(rows, 'Rows are present.')

    def testCircuitFetch(self):
        """
        """
        rows = []
        for row in self.aggregator._MSGDataAggregator__rawWeatherData(
                startDate = self.testStart, endDate = self.testEnd):
            rows.append(row)
        self.assertIsNotNone(rows, 'Rows are present.')

    def testEgaugeFetch(self):
        rows = []
        for row in self.aggregator._MSGDataAggregator__rawEgaugeData(
                startDate = self.testStart, endDate = self.testEnd):
            rows.append(row)
        self.assertIsNotNone(rows, 'Rows are present.')

    def testIrradianceAggregation(self):
        rowCnt = 0
        for row in self.aggregator.aggregatedIrradianceData(
                startDate = self.testStart, endDate = self.testEnd):
            print '%d %s' % (rowCnt, row)
            rowCnt += 1
        self.assertEqual(rowCnt, 20, 'Row count does not reflect four sensors.')

    def testWeatherAggregation(self):
        rowCnt = 0
        for row in self.aggregator.aggregatedWeatherData(
                startDate = self.testStart, endDate = self.testEnd):
            print '%d %s' % (rowCnt, row)
            rowCnt += 1


if __name__ == '__main__':
    RUN_SELECTED_TESTS = True

    if RUN_SELECTED_TESTS:
        selected_tests = ['testIrradianceAggregation', 'testWeatherAggregation']
        mySuite = unittest.TestSuite()
        for t in selected_tests:
            mySuite.addTest(MSGDataAggregatorTester(t))
        unittest.TextTestRunner().run(mySuite)
    else:
        unittest.main()
