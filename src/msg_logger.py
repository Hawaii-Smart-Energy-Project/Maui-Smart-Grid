#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'
__copyright__ = 'Copyright (c) 2013, University of Hawaii Smart Energy Project'
__license__ = 'https://raw.github' \
              '.com/Hawaii-Smart-Energy-Project/Maui-Smart-Grid/master/BSD' \
              '-LICENSE.txt'

import sys
import logging
from io import StringIO


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

        print "Initializing logger for %s." % caller

        self.logger = logging.getLogger(caller)

        self.ioStream = StringIO()

        #self.streamHandlerStdErr = logging.StreamHandler(sys.stderr)
        self.streamHandlerString = logging.StreamHandler(self.ioStream)
        #self.streamHandlerStdErr.setLevel(logging.DEBUG)
        self.streamHandlerString.setLevel(logging.DEBUG)

        formatterStdErr = logging.Formatter(
            u'%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        formatterString = logging.Formatter(
            u'string: %(asctime)s - %(name)s - %(levelname)s - %(message)s')

        #self.streamHandlerStdErr.setFormatter(formatterStdErr)
        self.streamHandlerString.setFormatter(formatterString)

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

        # Messages equal to and above the logging level will be logged.
        #
        # Override the given level for testing.
        self.logger.setLevel(logging.DEBUG)

        self.recording = []
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

        #for handler in self.logger.handlers:
        #    handler.flush()
        #    self.logger.removeHandler(handler)


        #self.logger.addHandler(self.streamHandlerStdErr)
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
            #print '%d: %s' % (self.logCounter, message)

            self.logger.log(loggerLevel, message)

            if self.shouldRecord:
                #self.logger.removeHandler(self.streamHandlerString)
                #self.streamHandlerString.flush()

                print u'%d -----> %s' % (
                self.logCounter, self.ioStream.getvalue())

                for handler in self.logger.handlers:
                    handler.flush()
                    self.ioStream.flush()
                    self.logger.removeHandler(handler)

                #self.recording += '%d:%s' % (
                #self.logCounter, self.ioStream.getvalue())

                self.recording.append(
                    '%d:%s' % (self.logCounter, self.ioStream.getvalue()))

                pass

            self.logCounter += 1

    def startRecording(self):
        self.shouldRecord = True

    def endRecording(self):
        self.shouldRecord = False
