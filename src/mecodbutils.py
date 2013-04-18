#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'

import sys

DEBUG = 1


class MECODBUtil(object):
    """Utility methods.
    """

    def __init__(self):
        """Constructor
        """

    def getLastSequenceID(self, conn, tableName, columnName):
        """Get last sequence ID value for the given sequence and for the
        given connection.
        :param conn: database connection
        :param tableName: name of the table that the sequence matches
        :param columnName: name of the column to which the sequence is applied
        :returns: last sequence value or None if not found
        """

        if DEBUG:
            print "table name = %s" % tableName
            print "column name = %s" % columnName

        sql = "select currval(pg_get_serial_sequence('\"%s\"','%s'))" % (
            tableName, columnName)

        cur = conn.cursor()
        self.executeSQL(cur, sql)
        row = cur.fetchone()
        lastSequenceValue = row[0]

        if lastSequenceValue is None:
            print"Critical error. Last sequence value could not be retrieved."
            sys.exit()

        return lastSequenceValue

    def executeSQL(self, cursor, sql):
        """Execute SQL given a cursor and a SQL statement.

        :param cursor Database cursor
        :param sql SQL statement
        :return True for success, False for failure
        """

        success = True
        try:
            cursor.execute(sql)
        except Exception, e:
            success = False
            print "execute failed with " + sql
            print "ERROR: ", e[0]
            print
            return False

        print "SQL execute was successful."

        return success

    def eraseTestMeco(self, dbCursor):
        sql = self.executeSQL(dbCursor, "select current_database()")
        row = dbCursor.fetchone()

        print "Erasing testing database %s." % row
        sql = ("""delete from "Reading";""",
               """delete from "Interval";""",
               """delete from "IntervalReadData";""",
               """delete from "MeterData";""",
               """SELECT setval('interval_id_seq', 1);""",
               """SELECT setval('intervalreaddata_id_seq', 1);""",
               """SELECT setval('meterdata_id_seq', 1);""",
               """SELECT setval('reading_id_seq', 1);""",
               """SELECT setval('register_id_seq', 1);""",
               """SELECT setval('registerdata_id_seq', 1);""",
               """SELECT setval('registerread_id_seq', 1);""",
               """SELECT setval('tier_id_seq', 1);""")

        for statement in sql:
            print "sql = %s" % statement
            self.executeSQL(dbCursor, statement)




