#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'

import sys

class MECOLogger(object):
    """
    """

    def __init__(self):
        """
        Constructor.
        """

        pass

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
