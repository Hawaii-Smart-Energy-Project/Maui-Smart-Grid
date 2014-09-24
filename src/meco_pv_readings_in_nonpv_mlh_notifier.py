#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Reports PV readings that are found to be new in the nonPV Meter Location
History.

This is not currently being used.
"""

__author__ = 'Daniel Zhang (張道博)'
__copyright__ = 'Copyright (c) 2013, University of Hawaii Smart Energy Project'
__license__ = 'https://raw.github' \
              '.com/Hawaii-Smart-Energy-Project/Maui-Smart-Grid/master/BSD' \
              '-LICENSE.txt'

from datetime import datetime as dt
from sek.logger import SEKLogger
from msg_notifier import MSGNotifier
from msg_db_connector import MSGDBConnector


class MECONonPVinMLHNotifier(object):
    def __init__(self):
        """
        Constructor.
        """

        self.logger = SEKLogger(__name__)
        self.viewPVReadingsinNonMLH = ''
        self.lastDateProcessed = None
        self.connector = MSGDBConnector()
        self.conn = self.connector.connectDB()

    def sendNewReadingsNotification(self):
        pass

    def checkForNewReadings(self, lastDate = None):
        sql = """SELECT * FROM %s """ % (self.viewPVReadingsinNonMLH)


if __name__ == '__main__':
    pass
