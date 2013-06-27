#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'

import sys
import logging


class MECOLogger(object):
    """
    This class provides logging functionality.
    """

    def __init__(self, caller, level):
        """
        Constructor.

        :params caller: Calling class.
        """

        self.logger = logging.getLogger(caller)
        self.logger.setLevel(logging.INFO)
        self.streamHandler = logging.StreamHandler(sys.stderr)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.streamHandler.setFormatter(formatter)

        self.loggerLevel = None
        if level == 'info':
            self.loggerLevel = logging.INFO
        elif level == 'error':
            self.loggerLevel = logging.ERROR
        elif level == 'silent':
            self.loggerLevel = None
        else:
            self.loggerLevel = None

        recordedLog = ''

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
        * error
        * silent

        :params message: A message to be logged.
        :params level: (optional) Logging level.
        """

        self.logger.addHandler(self.streamHandler)
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
            self.logger.removeHandler(self.streamHandler)
            # self.streamHandler.flush()

    def startRecording(self):
        pass

    def endRecording(self):
        pass
