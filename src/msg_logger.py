#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'
__copyright__ = 'Copyright (c) 2013, University of Hawaii Smart Energy Project'
__license__ = 'https://raw.github' \
              '.com/Hawaii-Smart-Energy-Project/Maui-Smart-Grid/master/BSD' \
              '-LICENSE.txt'

import sys
import logging
import StringIO


class MSGLogger(object):
    """
    This class provides logging functionality.
    """

    def __init__(self, caller, level = 'info'):
        """
        Constructor.

        :params caller: Calling class.
        :params level: An enumerated type detailing the level of the logging.

        @todo Provide enumeration type.
        """

        self.logger = logging.getLogger(caller)

        # Messages equal to and above the logging level will be logged.
        self.logger.setLevel(logging.DEBUG)
        self.ioStream = StringIO.StringIO()
        self.streamHandlerStdErr = logging.StreamHandler(sys.stderr)
        self.streamHandlerString = logging.StreamHandler(self.ioStream)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.streamHandlerStdErr.setFormatter(formatter)
        self.streamHandlerString.setFormatter(formatter)

        self.loggerLevel = None
        level = level.lower()
        if level == 'info':
            self.loggerLevel = logging.INFO
        elif level == 'error':
            self.loggerLevel = logging.ERROR
        elif level == 'silent':
            self.loggerLevel = None
        elif level == 'debug':
            self.loggerLevel = logging.DEBUG
        else:
            self.loggerLevel = None

        self.recording = ''
        self.shouldRecord = False


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

        if not level:
            loggerLevel = self.loggerLevel

        else:
            loggerLevel = None
            if level == 'info':
                loggerLevel = logging.INFO
            elif level == 'debug':
                loggerLevel = logging.DEBUG
            elif level == 'error':
                loggerLevel = logging.ERROR
            elif level == 'silent':
                loggerLevel = None
            else:
                loggerLevel = self.loggerLevel

        if loggerLevel != None:
            self.logger.log(loggerLevel, message)
            if self.shouldRecord:
                self.recording += self.ioStream.getvalue()
            self.logger.removeHandler(self.streamHandlerStdErr)
            self.logger.removeHandler(self.streamHandlerString)

    def startRecording(self):
        self.shouldRecord = True

    def endRecording(self):
        self.shouldRecord = False
