#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'
__copyright__ = 'Copyright (c) 2014, University of Hawaii Smart Energy Project'
__license__ = 'https://raw.github' \
              '.com/Hawaii-Smart-Energy-Project/Maui-Smart-Grid/master/BSD' \
              '-LICENSE.txt'

import unittest
from msg_time_util import MSGTimeUtil
import re
from sek.logger import SEKLogger
from datetime import datetime as dt


class MSGTimeUtilTester(unittest.TestCase):
    def setUp(self):
        self.logger = SEKLogger(__name__, 'debug')
        self.timeUtil = MSGTimeUtil()

    def test_concise_now(self):
        conciseNow = self.timeUtil.conciseNow()
        self.logger.log(conciseNow)
        pattern = '\d+-\d+-\d+_\d+'
        result = re.match(pattern, conciseNow)
        self.assertTrue(result is not None,
                        "Concise now matches the regex pattern.")

    def test_split_dates(self):
        start = dt(2014, 01, 07)
        end = dt(2014, 04, 04)
        print self.timeUtil.splitDates(start, end)
        self.assertEqual(len(self.timeUtil.splitDates(start, end)), 4,
                         'Unexpected date count.')


if __name__ == '__main__':
    unittest.main()
