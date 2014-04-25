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
from msg_notifier import MSGNotifier

class MSGDataAggregatorTester(unittest.TestCase):
    """
    Perform aggregation of new data.
    """

    def setUp(self):
        """
        Constructor.
        """
        self.logger = MSGLogger(__name__, 'DEBUG')
        self.aggregator = MSGDataAggregator()
        self.notifier = MSGNotifier()
        self.rawTypes = ['weather', 'egauge', 'circuit', 'irradiance']

    def testAggregateNewData(self):
        """
        :return:
        """

        msg = 'Aggregating new data.'

        result = map(self.aggregator.aggregateNewData, self.rawTypes)

        self.logger.log('result {}'.format(result))

if __name__ == '__main__':
    RUN_SELECTED_TESTS = True

    if RUN_SELECTED_TESTS:
        selected_tests = ['testAggregateNewData']
        mySuite = unittest.TestSuite()
        for t in selected_tests:
            mySuite.addTest(MSGDataAggregatorTester(t))
        unittest.TextTestRunner().run(mySuite)
    else:
        unittest.main()
