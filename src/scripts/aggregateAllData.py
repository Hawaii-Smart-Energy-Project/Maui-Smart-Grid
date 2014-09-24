#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Perform aggregation of all available data.

Usage:

1. Fill in self.rawTypes in __init__.

2. python aggregateAllData.py

This causes aggregated data to be inserted into the respective aggregated
data tables that are defined in the site-wide configuration file.

This was created to handle a special case where raw data became available
after the time of aggregation.

This script enables aggregation and loading of aggregated data while not
terminating when duplicate key errors are encountered.

The following flags invoked here, exitOnError
and commitOnEveryInsert, allow the ability to work around duplicate key
errors and the lack of commits due to errors occurring within a transaction.

"""

__author__ = 'Daniel Zhang (張道博)'
__copyright__ = 'Copyright (c) 2014, University of Hawaii Smart Energy Project'
__license__ = 'https://raw.github' \
              '.com/Hawaii-Smart-Energy-Project/Maui-Smart-Grid/master/BSD' \
              '-LICENSE.txt'

from sek.logger import SEKLogger
from msg_data_aggregator import MSGDataAggregator
from msg_notifier import MSGNotifier
from msg_db_connector import MSGDBConnector
from msg_db_util import MSGDBUtil


class AllDataAggregator(object):
    """
    Perform aggregation of all data for a set of predefined data types.

    In this class, the raw types are left as empty to allow manual
    specification.
    """

    def __init__(self):
        """
        Constructor.
        """
        self.logger = SEKLogger(__name__, 'DEBUG')
        self.aggregator = MSGDataAggregator(exitOnError = False,
                                            commitOnEveryInsert = True)
        self.notifier = MSGNotifier()

        # Available types are in ['weather', 'egauge', 'circuit', 'irradiance'].
        self.rawTypes = ['']
        self.connector = MSGDBConnector()
        self.conn = self.connector.connectDB()
        self.cursor = self.conn.cursor()
        self.dbUtil = MSGDBUtil()

    def aggregateAllData(self):
        """
        :return: Nothing.
        """

        map(self.aggregator.aggregateAllData, self.rawTypes)


if __name__ == '__main__':
    aggregator = AllDataAggregator()
    logger = SEKLogger(__name__)
    result = aggregator.aggregateAllData()

