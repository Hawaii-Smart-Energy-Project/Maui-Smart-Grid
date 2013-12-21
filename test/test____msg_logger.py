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
        #print "Initializing logger."
        self.logger = MSGLogger(__name__, level='DEBUG')
        print 'logger level: %s' % self.logger.loggerLevel

    def testInit(self):
        self.logger.log('Testing init.',level='info')

        self.assertIsNotNone(self.logger)

    def testLogRecording(self):
        self.logger.log('Testing log recording.','info')

        msg = "Recording test."

        self.logger.startRecording()
        self.logger.log(msg, INFO)
        self.logger.endRecording()
        self.logger.log("This should not be logged.", INFO)

        self.assertEqual(self.logger.recording, msg)

    def testSilentLogging(self):
        self.logger.log('Testing silent logging.','info')

        msg = "Recording test."

        self.logger.startRecording()
        self.logger.log(msg, 'silent')
        self.logger.endRecording()

        self.assertEqual(self.logger.recording, '')

    def testDebugLogging(self):
        self.logger.log('Testing debug logging','DEBUG')


if __name__ == '__main__':
    unittest.main()
