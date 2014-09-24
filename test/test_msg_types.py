#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'
__copyright__ = 'Copyright (c) 2014, University of Hawaii Smart Energy Project'
__license__ = 'https://raw.github' \
              '.com/Hawaii-Smart-Energy-Project/Maui-Smart-Grid/master/BSD' \
              '-LICENSE.txt'

import unittest
from sek.logger import SEKLogger
from msg_types import MSGAggregationTypes


class MSGTypesTester(unittest.TestCase):
    """
    Unit tests for MSG Aggregation Types.
    """

    def setUp(self):
        self.logger = SEKLogger(__name__, 'DEBUG')

    def test_aggregation_types(self):
        self.assertTrue(MSGAggregationTypes.weather in MSGAggregationTypes)
        self.assertTrue(MSGAggregationTypes.egauge in MSGAggregationTypes)
        self.assertTrue(MSGAggregationTypes.circuit in MSGAggregationTypes)
        self.assertTrue(MSGAggregationTypes.irradiance in MSGAggregationTypes)

    def tearDown(self):
        pass


if __name__ == '__main__':
    RUN_SELECTED_TESTS = True

    if RUN_SELECTED_TESTS:

        selected_tests = ['test_aggregation_types']

        mySuite = unittest.TestSuite()
        for t in selected_tests:
            mySuite.addTest(MSGTypesTester(t))
        unittest.TextTestRunner().run(mySuite)
    else:
        unittest.main()
