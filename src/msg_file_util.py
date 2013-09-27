#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'
__copyright__ = 'Copyright (c) 2013, University of Hawaii Smart Energy Project'
__license__ = 'https://raw.github' \
              '.com/Hawaii-Smart-Energy-Project/Maui-Smart-Grid/master/BSD' \
              '-LICENSE.txt'

from msg_logger import MSGLogger
import os

class MSGFileUtil(object):
    """
    Utilities related to files and directories.
    """

    def __init__(self):
        """
        Constructor.
        """
        self.logger = MSGLogger(__name__)


    def validDirectory(self, path):
        """
        Verify that the path is a valid directory.

        :returns: True if path is a valid directory.
        """
        if os.path.exists(path) and os.path.isdir(path):
            return True
        else:
            return False
