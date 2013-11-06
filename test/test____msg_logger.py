#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'

import unittest
from msg_logger import MSGLogger
from logging import INFO
from logging import DEBUG
from logging import ERROR


class MSGLoggerTester(unittest.TestCase):

    def setUp(self):
        self.logger = MSGLogger(__name__)

    def testInit(self):
        self.assertIsNotNone(self.logger)

    def testLogRecording(self):
        msg = "Recording test."

        self.logger.startRecording()
        self.logger.log(msg, INFO)
        self.logger.endRecording()
        self.logger.log("This should not be logged.", INFO)

        self.assertEqual(self.logger.recording, msg)
        

if __name__ == '__main__':
    unittest.main()
