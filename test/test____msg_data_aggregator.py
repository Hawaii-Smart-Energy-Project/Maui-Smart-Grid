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
from msg_aggregated_data import MSGAggregatedData


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
        self.testEnd = '2014-01-02 12:59'

    def testIrradianceFetch(self):
        """
        """
        timeCol = 'timestamp'
        rows = []
        for row in self.aggregator._MSGDataAggregator__rawData(
                dataType = 'irradiance', orderBy = [timeCol, 'sensor_id'],
                timestampCol = timeCol, startDate = self.testStart,
                endDate = self.testEnd):
            rows.append(row)
        self.assertIsNotNone(rows, 'Rows are present.')

    def testWeatherFetch(self):
        """
        """
        timeCol = 'timestamp'
        rows = []
        for row in self.aggregator._MSGDataAggregator__rawData(
                dataType = 'weather', orderBy = [timeCol],
                timestampCol = timeCol, startDate = self.testStart,
                endDate = self.testEnd):
            rows.append(row)
        self.assertIsNotNone(rows, 'Rows are present.')

    def testCircuitFetch(self):
        """
        """
        timeCol = 'timestamp'
        rows = []
        for row in self.aggregator._MSGDataAggregator__rawData(
                dataType = 'circuit', orderBy = [timeCol, 'circuit'],
                timestampCol = timeCol, startDate = self.testStart,
                endDate = self.testEnd):
            rows.append(row)
        self.assertIsNotNone(rows, 'Rows are present.')

    def testEgaugeFetch(self):
        timeCol = 'datetime'
        rows = []
        for row in self.aggregator._MSGDataAggregator__rawData(
                dataType = 'egauge', orderBy = [timeCol, 'egauge_id'],
                timestampCol = timeCol, startDate = self.testStart,
                endDate = self.testEnd):
            rows.append(row)
        self.assertIsNotNone(rows, 'Rows are present.')

    def testIrradianceAggregation(self):
        rowCnt = 0
        for row in self.aggregator.aggregatedIrradianceData(
                startDate = self.testStart, endDate = self.testEnd).data:
            print '%d: %s' % (rowCnt, row)
            rowCnt += 1
        self.assertEqual(rowCnt, self.aggregator.irradianceSensorCount * 4,
                         'Row count does not reflect four sensors.')

    def testWeatherAggregation(self):
        rowCnt = 0
        for row in self.aggregator.aggregatedWeatherData(
                startDate = self.testStart, endDate = self.testEnd).data:
            print '%d: %s' % (rowCnt, row)
            rowCnt += 1

    def testCircuitAggregation(self):
        rowCnt = 0

        for row in self.aggregator.aggregatedCircuitData(
                startDate = self.testStart, endDate = self.testEnd).data:
            print row
            rowCnt += 1

        self.assertEqual(rowCnt, 4,
                         'Rows are not equal to the number of intervals.')


    def testEgaugeAggregation(self):
        rowCnt = 0

        for row in self.aggregator.aggregatedEgaugeData(
                startDate = self.testStart, endDate = self.testEnd).data:
            print row
            rowCnt += 1

            # self.assertEqual(rowCnt, 4,
            #                  'Rows are not equal to the number of intervals.')

    def testWriteIrradianceAggregation(self):
        # self.aggregator._MSGDataAggregator__writeAggregatedData(
        # dataType='irradiance', aggDataCols)
        pass


if __name__ == '__main__':
    RUN_SELECTED_TESTS = True

    if RUN_SELECTED_TESTS:
        selected_tests = ['testWeatherAggregation', 'testIrradianceAggregation',
                          'testEgaugeAggregation', 'testCircuitAggregation',
                          'testCircuitFetch']
        mySuite = unittest.TestSuite()
        for t in selected_tests:
            mySuite.addTest(MSGDataAggregatorTester(t))
        unittest.TextTestRunner().run(mySuite)
    else:
        unittest.main()
