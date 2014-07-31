#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'

import unittest
from msg_logger import MSGLogger

# @todo Replace strings with enumeration types.
from logging import INFO
from logging import DEBUG
from logging import ERROR

import re


class MSGLoggerTester(unittest.TestCase):

    def setUp(self):
        self.logger = MSGLogger(__name__, level='DEBUG')
        print 'logger level: %s' % self.logger.loggerLevel

    def testInit(self):
        self.logger.log('Testing init.',level='info')

        self.assertIsNotNone(self.logger)

    def testLogRecording(self):
        self.logger.log('Testing log recording.','info')

        msg = "Recording test."

        self.logger.startRecording()
        self.logger.log(msg, 'info')
        self.logger.endRecording()
        self.logger.log("This should not be logged.", 'info')

        result = re.search(msg, self.logger.recording).group(0)

        self.logger.log("recording result: %s" % self.logger.recording)

        self.assertEqual(result, msg)

    def testSilentLogging(self):
        return

        self.logger.log('Testing silent logging.','info')

        msg = "Recording test."

        self.logger.startRecording()
        self.logger.log(msg, 'silent')
        self.logger.endRecording()

        self.assertEqual(self.logger.recording, '')

    def testDebugLogging(self):
        self.logger.log('Testing debug logging','DEBUG')

    def testDoublingOfLoggingOutput(self):
        self.logger.log('This is a test of doubling of logger output at the beginning of a test.')


if __name__ == '__main__':
    unittest.main()
