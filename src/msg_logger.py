#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Provide logging services for the MSG Data Operations Project.

Setting self.shouldRecord=True provides a way of collecting all logging output
for the instantiated logger into self.recording.
"""

__author__ = 'Daniel Zhang (張道博)'
__copyright__ = 'Copyright (c) 2013, University of Hawaii Smart Energy Project'
__license__ = 'https://raw.github' \
              '.com/Hawaii-Smart-Energy-Project/Maui-Smart-Grid/master/BSD' \
              '-LICENSE.txt'

import sys
import logging
from io import StringIO


def enum(**enums):
    return type('Enum', (), enums)


class MSGLogger(object):
    """
    This class provides logging functionality.

    It supports recording of log output by setting self.shouldRecord = True.
    The recorded output is then available in self.recording.

    :param caller: The object that is calling this class.
    :param level: Logger level string in ('info', 'error', 'silent', 'debug')
    """

    def __init__(self, caller, level = 'info'):
        """
        Constructor.

        :params caller: Calling class.
        :params level: Logging level of the Logger.

        @todo Provide enumeration type.
        """

        self.logger = logging.getLogger(caller)

        self.ioStream = StringIO()

        self.streamHandlerStdErr = logging.StreamHandler(sys.stderr)
        self.streamHandlerString = logging.StreamHandler(self.ioStream)
        self.streamHandlerStdErr.setLevel(logging.DEBUG)
        self.streamHandlerString.setLevel(logging.DEBUG)

        formatterStdErr = logging.Formatter(
            u'%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        formatterString = logging.Formatter(
            u'%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        self.streamHandlerStdErr.setFormatter(formatterStdErr)
        self.streamHandlerString.setFormatter(formatterString)

        self.loggerLevel = None

        #The log level that is set here provides the cut-off point for future
        # calls to log that are responsible for the actual log messages.

        # The log level here has a slightly different meaning than the log
        # level used in the call to self.logger.log().

        level = level.lower()

        if level == 'info':
            self.loggerLevel = logging.INFO
        elif level == 'error':
            self.loggerLevel = logging.ERROR
        elif level == 'silent':
            self.loggerLevel = logging.NOTSET
        elif level == 'debug':
            self.loggerLevel = logging.DEBUG
        else:
            self.loggerLevel = logging.INFO


        # Messages equal to and above the logging level will be logged.

        # Setting the level here is essential to get output from the logger.
        self.logger.setLevel(self.loggerLevel)

        self.recordingBuffer = []
        self.recording = ''
        self.shouldRecord = False
        self.logCounter = 0


    def logAndWrite(self, message):
        """
        With a given string, write it to stderr and return its value for
        appending to a running log.

        Nothing is added to the message. Therefore, if linefeeds are desired
        they should be included explicitly.

        :param message: A string message to be logged.
        :returns: The message.
        """

        sys.stderr.write(message)
        return message


    def log(self, message, level = None):
        """
        Write a log message.

        Logging levels are

        * info
        * debug
        * error
        * silent

        :params message: A message to be logged.
        :params level: (optional) Logging level.
        """

        self.logger.addHandler(self.streamHandlerStdErr)
        self.logger.addHandler(self.streamHandlerString)

        if level:
            level = level.lower()

        #loggerLevel = None
        if level == 'info':
            loggerLevel = logging.INFO
        elif level == 'debug':
            loggerLevel = logging.DEBUG
        elif level == 'error':
            loggerLevel = logging.ERROR
        elif level == 'silent':
            loggerLevel = logging.NOTSET
        else:
            loggerLevel = logging.INFO # Default logger level.

        if loggerLevel != None:
            # For debugging:
            #print 'message: %s, logger level: %s' % (message, loggerLevel)
            self.logger.log(loggerLevel, message)

            if self.shouldRecord:
                # The recording buffer is a cumulative copy of the logging
                # output. At each iteration, the buffer plus the new output is
                # appended to the list.
                self.recordingBuffer.append('%s' % (self.ioStream.getvalue()))
                self.recording = self.recordingBuffer[-1]

            for handler in self.logger.handlers:
                # The flushes here apparently don't have any effect on the
                # logger.
                handler.flush()
                self.ioStream.flush()
                self.logger.removeHandler(handler)

            self.logCounter += 1
        else:
            # @todo Add assert for invalid log level.
            print "Invalid logger level."


    def startRecording(self):
        self.shouldRecord = True

    def endRecording(self):
        self.shouldRecord = False
