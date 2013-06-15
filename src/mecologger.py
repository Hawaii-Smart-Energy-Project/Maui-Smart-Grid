#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'

import sys
import logging


class MECOLogger(object):
    """
    This class provides logging functionality.
    """

    def __init__(self):
        """
        Constructor.
        """

        self.logger = logging.getLogger('MSG-Data-Processing')
        self.logger.setLevel(logging.DEBUG)
        self.streamHandler = logging.StreamHandler(sys.stderr)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.streamHandler.setFormatter(formatter)
        self.logger.addHandler(self.streamHandler)

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

    def log(self, message):
        """
        Write a log message.

        :params message: A message to be logged.
        """

        self.logger.log(logging.INFO, message)
        self.streamHandler.flush()
