#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'

from mecodbconnect import MECODBConnector
from mecodbutils import MECODBUtil
import psycopg2
import psycopg2.extras

class MECODBReader(object) :
    """Read records from a database.
    """

    def __init__(self) :
        """Constructor
        """

        self.conn = MECODBConnector().connectDB()
        self.dbUtil = MECODBUtil()

    def selectRecord(self, conn, table, keyName, keyValue) :
        """Read a record in the database given a table name, primary
        key name, and value for the key.

        :param conn DB connection
        :param table DB table name
        :param keyName DB column name for primary key
        :param keyValue Value to be matched
        """

        print "selectRecord:"
        sql = 'select * from \"%s\" where %s = %s' % (table, keyName, keyValue)
        dcur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
        self.dbUtil.executeSQL(dcur, sql)
        row = dcur.fetchone()
        return row



