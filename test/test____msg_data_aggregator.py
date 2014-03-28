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
        self.testStart = '2014-01-02 11:59'
        self.testEnd = '2014-01-02 12:14'

    def testIrradianceFetch(self):
        """
        Test raw data fetching over the testing time interval.
        :return:
        """

        timeCol = 'timestamp'
        rows = []
        for row in self.aggregator.rawData(dataType = 'irradiance',
                                           orderBy = [timeCol, 'sensor_id'],
                                           timestampCol = timeCol,
                                           startDate = self.testStart,
                                           endDate = self.testEnd):
            rows.append(row)
        self.assertIsNotNone(rows, 'Rows are present.')

    def testWeatherFetch(self):
        """
        Test raw data fetching over the testing time interval.
        :return:
        """

        timeCol = 'timestamp'
        rows = []
        for row in self.aggregator.rawData(dataType = 'weather',
                                           orderBy = [timeCol],
                                           timestampCol = timeCol,
                                           startDate = self.testStart,
                                           endDate = self.testEnd):
            rows.append(row)
        self.assertIsNotNone(rows, 'Rows are present.')

    def testCircuitFetch(self):
        """
        Test raw data fetching over the testing time interval.
        :return:
        """

        timeCol = 'timestamp'
        rows = []
        for row in self.aggregator.rawData(dataType = 'circuit',
                                           orderBy = [timeCol, 'circuit'],
                                           timestampCol = timeCol,
                                           startDate = self.testStart,
                                           endDate = self.testEnd):
            rows.append(row)
        self.assertIsNotNone(rows, 'Rows are present.')

    def testEgaugeFetch(self):
        """
        Test raw data fetching over the testing time interval.
        :return:
        """

        timeCol = 'datetime'
        rows = []
        for row in self.aggregator.rawData(dataType = 'egauge',
                                           orderBy = [timeCol, 'egauge_id'],
                                           timestampCol = timeCol,
                                           startDate = self.testStart,
                                           endDate = self.testEnd):
            rows.append(row)
        self.assertIsNotNone(rows, 'Rows are present.')


    def testEgaugeAggregation(self):
        """
        Perform aggregation over the testing time interval.
        :return:
        """

        self.logger.log('Testing Egauge aggregation.')
        rowCnt = 0
        agg = self.aggregator.aggregatedData(dataType = 'egauge',
                                             aggregationType = 'agg_egauge',
                                             timeColumnName = 'datetime',
                                             subkeyColumnName = 'egauge_id',
                                             startDate = self.testStart,
                                             endDate = self.testEnd)
        print [col for col in agg.columns]
        for row in agg.data:
            print row
            rowCnt += 1
        self.logger.log('row cnt %d' % rowCnt)
        self.logger.log('agg cols: %d' % len(agg.columns))
        self.assertEqual(rowCnt, 5, 'Row count not correct.')

        self.assertEqual(len(agg.columns), 37,
                         'Egauge columns not equal to 37.')
        self.aggregator.insertAggregatedData(agg = agg)


    def testCircuitAggregation(self):
        """
        Test aggregation over the testing time interval.
        :return:
        """

        self.logger.log('Testing circuit aggregation.')
        rowCnt = 0
        agg = self.aggregator.aggregatedData(dataType = 'circuit',
                                             aggregationType = 'agg_circuit',
                                             timeColumnName = 'timestamp',
                                             subkeyColumnName = 'circuit',
                                             startDate = self.testStart,
                                             endDate = self.testEnd)
        print [col for col in agg.columns]
        for row in agg.data:
            print row
            rowCnt += 1
        self.logger.log('row cnt %d' % rowCnt)
        self.logger.log('agg cols: %d' % len(agg.columns))
        self.assertEqual(rowCnt, 2, 'Row count not correct.')
        self.assertEqual(len(agg.columns), 8, 'Circuit columns not equal to 8.')
        self.aggregator.insertAggregatedData(agg = agg)


    def testIrradianceAggregation(self):
        """
        Test aggregation over the testing time interval.
        :return:
        """

        self.logger.log('Testing irradiance aggregation.')
        rowCnt = 0
        datatype = 'irradiance'
        agg = self.aggregator.aggregatedData(dataType = datatype,
                                             aggregationType = 'agg_irradiance',
                                             timeColumnName = 'timestamp',
                                             subkeyColumnName = 'sensor_id',
                                             startDate = self.testStart,
                                             endDate = self.testEnd)
        for row in agg.data:
            print '%d: %s' % (rowCnt, row)
            rowCnt += 1
        self.logger.log('row cnt %d' % rowCnt)
        self.logger.log('agg cols: %d' % len(agg.columns))
        self.assertEqual(rowCnt, 1, 'Row count not correct.')
        self.assertEqual(len(agg.columns), 3,
                         'Irradiance columns not equal to 3.')
        self.aggregator.insertAggregatedData(agg = agg)


    def testWeatherAggregation(self):
        """
        Test aggregation over the testing time interval.
        :return:
        """

        rowCnt = 0
        agg = self.aggregator.aggregatedData(dataType = 'weather',
                                             aggregationType = 'agg_weather',
                                             timeColumnName = 'timestamp',
                                             subkeyColumnName = None,
                                             startDate = self.testStart,
                                             endDate = self.testEnd)
        for row in agg.data:
            print '%d: %s' % (rowCnt, row)
            rowCnt += 1
        self.assertEqual(rowCnt, 1, 'Row count not correct.')

        self.logger.log('agg cols: %d' % len(agg.columns))
        self.assertEqual(len(agg.columns), 3, 'Weather columns not equal to 3.')
        self.aggregator.insertAggregatedData(agg = agg)


    def testMonthStartsAndEnds(self):
        """
        Test retrieving the list of start and end dates for each month in a
        given aggregation time period.
        :return:
        """

        for myType in ['weather', 'egauge', 'circuit', 'irradiance']:
            if myType == 'egauge':
                print self.aggregator.monthStartsAndEnds(
                    timeColumnName = 'datetime', dataType = myType)
            else:
                print self.aggregator.monthStartsAndEnds(
                    timeColumnName = 'timestamp', dataType = myType)


    def testAggregateAllData(self):

        # @todo Revise this test so that live data is not affected.

        return

        for myType in ['weather', 'egauge', 'circuit', 'irradiance']:
            self.aggregator.aggregateAllData(dataType = myType)

    def testExistingIntervals(self):
        self.logger.log('Testing existing intervals.')
        aggType = [('agg_weather', 'timestamp'), ('agg_egauge', 'datetime'),
                   ('agg_circuit', 'timestamp'),
                   ('agg_irradiance', 'timestamp')]
        assert len(
            map(lambda x: self.aggregator.existingIntervals(x[0], x[1])[0],
                aggType)) == len(
            aggType), 'Mismatched existing aggregation intervals.'


if __name__ == '__main__':
    RUN_SELECTED_TESTS = True

    if RUN_SELECTED_TESTS:

        selected_tests = ['testWeatherAggregation', 'testEgaugeAggregation',
                          'testIrradianceAggregation', 'testCircuitAggregation']
        # selected_tests = ['testAggregateAllData']
        selected_tests = ['testExistingIntervals']

        mySuite = unittest.TestSuite()

        for t in selected_tests:
            mySuite.addTest(MSGDataAggregatorTester(t))
        unittest.TextTestRunner().run(mySuite)
    else:
        unittest.main()
