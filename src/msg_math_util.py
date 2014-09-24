#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'
__copyright__ = 'Copyright (c) 2013, University of Hawaii Smart Energy Project'
__license__ = 'https://raw.github' \
              '.com/Hawaii-Smart-Energy-Project/Maui-Smart-Grid/master/BSD' \
              '-LICENSE.txt'

from sek.logger import SEKLogger


class MSGMathUtil(object):
    """
    Math related utility methods.
    """

    def __init__(self):
        """
        Constructor.
        """
        self.logger = SEKLogger(__name__)

    def isNumber(self, s):
        try:
            float(s)
            return True
        except (TypeError, ValueError):
            return False
