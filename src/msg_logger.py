#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Provides logging services for the MSG Data Operations Project.

Setting self.shouldRecord=True provides a way of collecting all logging output
for the instantiated logger into self.recording.

Usage:

from msg_logger import MSGLogger
self.logger = MSGLogger(__name__)

The logger level is configurable by passing a predefined logging level.

    self.logger = MSGLogger(__name__, '${LOGGING_LEVEL}')

The name parameter is used to pass the calling class. The optional logging level
level corresponds to the levels used in the logging module. It is useful for
filtering logging output. For example, if the logger is instantiated using

    self.logger = MSGLogger(__name__, 'INFO')

then debugging level logging statements such as

    self.logger.log('A debug message.', 'DEBUG')

will not be printed.

Important Note:
The logging level is individually configured for each class where it is
instantiated. Getting the desired output requires setting the level within
each instance.

Public API:

log(message:String, level:String)
    Output a logging message at the specified logging level.

startRecoring()
    Starting recording of log messages to self.recording.

endRecording()
    End recording of log messages.

"""

__author__ = 'Daniel Zhang (張道博)'
__copyright__ = 'Copyright (c) 2014, University of Hawaii Smart Energy Project'
__license__ = 'https://raw.github' \
              '.com/Hawaii-Smart-Energy-Project/Maui-Smart-Grid/master/BSD' \
              '-LICENSE.txt'

import sys
import logging
from io import StringIO
from colorlog import ColoredFormatter


def enum(**enums):
    return type('Enum', (), enums)


class MSGLogger(object):
    """
    This class provides logging functionality.

    It supports recording of log output by setting self.shouldRecord = True.
    The recorded output is then available in self.recording.

    """

    def __init__(self, caller, level = 'info', useColor = True):
        """
        Constructor.

        :param caller: Object that is calling this class.
        :param level: String for logger level in ('info', 'error', 'warning',
        'silent', 'debug', 'critical')
        :param useColor: Boolean if True, color output is used via colorlog.

        @todo Provide enumeration type.
        """

        self.logger = logging.getLogger(caller)

        self.ioStream = StringIO()

        self.streamHandlerStdErr = logging.StreamHandler(sys.stderr)
        self.streamHandlerString = logging.StreamHandler(self.ioStream)
        self.streamHandlerStdErr.setLevel(logging.DEBUG)
        self.streamHandlerString.setLevel(logging.DEBUG)

        formatterString = logging.Formatter(
            u'%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        if not useColor:
            formatterStdErr = logging.Formatter(
                u'%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        else:
            # Use colored output:
            formatterStdErr = ColoredFormatter(
                u'%(log_color)s%(asctime)s - %(name)s - %(bold)s%(levelname)s: '
                u'%(reset)s%(message)s', reset = True,
                log_colors = {'DEBUG': 'green', 'INFO': 'blue',
                              'WARNING': 'yellow', 'ERROR': 'red',
                              'CRITICAL': 'red', })

        self.streamHandlerStdErr.setFormatter(formatterStdErr)
        self.streamHandlerString.setFormatter(formatterString)

        self.loggerLevel = None

        # The log level that is set here provides the cut-off point for future
        # calls to log that are responsible for the actual log messages.

        # The log level here has a slightly different meaning than the log
        # level used in the call to self.logger.log().

        level = level.lower()

        if level == 'info':
            self.loggerLevel = logging.INFO
        elif level == 'warning':
            self.loggerLevel = logging.WARNING
        elif level == 'error':
            self.loggerLevel = logging.ERROR
        elif level == 'silent':
            self.loggerLevel = logging.NOTSET
        elif level == 'debug':
            self.loggerLevel = logging.DEBUG
        elif level == 'critical':
            loggerLevel = logging.CRITICAL
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

        :param message: String message to be logged.
        :returns: String for the message.
        """

        sys.stderr.write(message)
        return message


    def log(self, message = '', level = None, color = None):
        """
        Write a log message.

        Logging levels are

        * info
        * debug
        * error
        * silent

        :param message: String for a message to be logged.
        :param level: String for an optional logging level.
        :param color: not supported yet.
        """

        self.logger.addHandler(self.streamHandlerStdErr)
        if self.shouldRecord:
            self.logger.addHandler(self.streamHandlerString)

        if level:
            level = level.lower()

        if level == 'info':
            loggerLevel = logging.INFO
        elif level == 'warning':
            loggerLevel = logging.WARNING
        elif level == 'debug':
            loggerLevel = logging.DEBUG
        elif level == 'error':
            loggerLevel = logging.ERROR
        elif level == 'silent':
            loggerLevel = logging.NOTSET
        elif level == 'critical':
            loggerLevel = logging.CRITICAL
        else:
            loggerLevel = logging.INFO  # Default logger level.

        if loggerLevel != None:
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
            raise Exception("Invalid logger level {}.".format(level))


    def startRecording(self):
        self.shouldRecord = True

    def endRecording(self):
        self.shouldRecord = False
