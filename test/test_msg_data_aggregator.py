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
from datetime import datetime
import itertools
from pprint import pprint


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
        self.rawTypes = ['weather', 'egauge', 'circuit', 'irradiance']

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


    def test_month_starts_and_ends(self):
        """
        Test retrieving the list of start and end dates for each month in a
        given aggregation time period.

        All starts except one should be at time 00:00:00.

        Starts and ends appear in alternating order but are joined in a tuple.
        """
        # @REVIEWED
        # @todo Optimize by combine start and end tests.

        startCnt = 0
        endCnt = 0

        def test_starts(timeColName, dataType):
            global startCnt
            self.logger.log('testing {},{}'.format(timeColName, dataType))

            # Take every other value from the unzipped pairs.
            starts = [x for x in itertools.islice(
                zip(*self.aggregator.monthStartsAndEnds(timeColName, dataType)),
                0, None, 2)]
            startCnt = len(starts)

            # Test on the flattened start values.
            self.assertLessEqual(len(filter(
                lambda x: x.time() != datetime.strptime('00:00:00',
                                                        '%H:%M:%S').time(),
                list(itertools.chain.from_iterable(starts)))), 1)

        def test_ends(timeColName, dataType):
            global endCnt
            self.logger.log('testing {},{}'.format(timeColName, dataType))

            # Take every other value from the unzipped pairs.
            ends = [x for x in itertools.islice(
                zip(*self.aggregator.monthStartsAndEnds(timeColName, dataType)),
                1, None, 2)]
            endCnt = len(ends)

            # Test on the flattened end values.
            self.assertLessEqual(len(filter(
                lambda x: x.time() != self.aggregator.incrementEndpoint(
                    datetime.strptime('23:59:59', '%H:%M:%S')).time(),
                list(itertools.chain.from_iterable(ends)))), 1)

        for myType in ['weather', 'egauge', 'circuit', 'irradiance']:
            if myType == 'egauge':
                test_starts('datetime', myType)
                test_ends('datetime', myType)
            else:
                test_starts('timestamp', myType)
                test_ends('timestamp', myType)
            self.assertEquals(startCnt, endCnt)


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
        self.assertEqual(len(
            map(lambda x: self.aggregator.existingIntervals(x[0], x[1])[0],
                aggType)) == len(aggType),
                         'Mismatched existing aggregation intervals.')

    def testUnaggregatedIntervals1(self):
        # @todo provide static test data for this test.
        self.logger.log('testing unagged intervals')
        MINUTE_POSITION = 4
        INTERVAL_DURATION = 15

        weather = []
        for row in self.aggregator.unaggregatedEndpoints('weather',
                                                         'agg_weather',
                                                         'timestamp'):
            self.logger.log('row: {}'.format(row))


    def testUnaggregatedIntervals2(self):
        # @todo provide static test data for this test.
        self.logger.log('testing unagged intervals')
        MINUTE_POSITION = 4
        INTERVAL_DURATION = 15

        egauge = []
        for row in self.aggregator.unaggregatedEndpoints('egauge', 'agg_egauge',
                                                         'datetime',
                                                         'egauge_id'):
            self.logger.log('row: {}'.format(row))


    def testLastAggregationEndpoint(self):
        # Covered by testUnaggregatedIntervals.
        self.logger.log('Testing last agg endpoint')
        print self.aggregator.lastAggregationEndpoint(aggDataType = 'weather',
                                                      timeColumnName =
                                                      'timestamp')

    def testUnaggregatedDataExists(self):
        """

        :return:
        """
        # @todo provide static test data for this test.

        myArgs = [('weather', 'agg_weather', 'timestamp', ''),
                  ('egauge', 'agg_egauge', 'datetime', 'egauge_id'),
                  ('circuit', 'agg_circuit', 'timestamp', 'circuit'),
                  ('irradiance', 'agg_irradiance', 'timestamp', 'sensor_id')]
        self.logger.log(map(
            lambda x: self.aggregator.unaggregatedIntervalCount(dataType = x[0],
                                                                aggDataType = x[
                                                                    1],
                                                                timeColumnName =
                                                                x[2],
                                                                idColumnName =
                                                                x[3]), myArgs))

    def testAggregatedVsNewData(self):
        """

        :return:
        """
        # @todo provide static test data for this test.

        result = self.aggregator.aggregatedVsNewData()

        self.logger.log('result {}'.format(result), 'info')
        self.assertEqual(len(self.aggregator.dataParams.keys()),
                         len(result.keys()),
                         'Result not obtained for each type.')

    def testAggregateNewData(self):
        """
        @IMPORTANT Should not be run on live data.
        :return:
        """

        # return
        map(self.aggregator.aggregateNewData, self.rawTypes)


    def testLastUnaggregatedAndAggregatedEndpoints(self):
        """
        :return:
        """
        # @todo Needs static test data.
        print self.aggregator.lastUnaggregatedAndAggregatedEndpoints(
            dataType = 'egauge')

    def test_endpoint_increment(self):
        myDT = datetime(2014, 02, 01, 23, 45)
        self.logger.log('dt = {}'.format(myDT))
        result = self.aggregator.incrementEndpoint(endpoint = myDT)
        self.logger.log('result {}'.format(result))
        self.assertEqual(result, datetime(2014, 02, 02, 00, 00, 00))


if __name__ == '__main__':
    RUN_SELECTED_TESTS = True

    if RUN_SELECTED_TESTS:
        selected_tests = ['test_month_starts_and_ends']
        mySuite = unittest.TestSuite()

        for t in selected_tests:
            mySuite.addTest(MSGDataAggregatorTester(t))
        unittest.TextTestRunner().run(mySuite)
    else:
        unittest.main()
