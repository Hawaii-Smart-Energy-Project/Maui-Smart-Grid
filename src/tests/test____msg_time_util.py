#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'

import unittest
from msg_time_util import MSGTimeUtil
import re
from msg_logger import MSGLogger

class MSGTimeUtilTester(unittest.TestCase):
    def setUp(self):
        self.logger = MSGLogger(__name__)
        self.timeUtil = MSGTimeUtil()

    def test_concise_now(self):
        conciseNow = self.timeUtil.conciseNow()
        self.logger.log(conciseNow)
        pattern = '\d+-\d+-\d+_\d+'
        result = re.match(pattern, conciseNow)
        self.assertTrue(result is not None, "Concise now matches the regex pattern.")


if __name__ == '__main__':
    unittest.main()
