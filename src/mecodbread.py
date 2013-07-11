#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'

from mecodbconnect import MECODBConnector
from msg_db_util import MSGDBUtil
import psycopg2
import psycopg2.extras


class MECODBReader(object):
    """
    Read records from a database.
    """

    def __init__(self, testing = False):
        """
        Constructor.

        :param testing: True if in testing mode.
        """

        self.connector = MECODBConnector()
        self.conn = MECODBConnector(testing).connectDB()
        self.dbUtil = MSGDBUtil()
        self.dbName = self.dbUtil.getDBName(self.connector.dictCur)

    def selectRecord(self, conn, table, keyName, keyValue):
        """
        Read a record in the database given a table name, primary key name,
        and value for the key.

        :param conn DB connection
        :param table DB table name
        :param keyName DB column name for primary key
        :param keyValue Value to be matched
        :returns: Row containing record data.
        """

        print "selectRecord:"
        sql = 'select * from \"%s\" where %s = %s' % (table, keyName, keyValue)
        dcur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
        self.dbUtil.executeSQL(dcur, sql)
        row = dcur.fetchone()
        return row

    def readingAndMeterCounts(self):
        """
        Retrieve the reading and meter counts.

        :returns: Multiple lists containing the retrieved data.
        """

        sql = """select "Day", "Reading Count",
        "Meter Count" from count_of_readings_and_meters_by_day"""
        dcur = self.conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
        self.dbUtil.executeSQL(dcur, sql)
        rows = dcur.fetchall()

        dates = []
        meterCounts = []
        readingCounts = []

        for row in rows:
            dates.append(row[0])
            readingCounts.append(row[1] / row[2])
            meterCounts.append(row[2])

        return dates, readingCounts, meterCounts
