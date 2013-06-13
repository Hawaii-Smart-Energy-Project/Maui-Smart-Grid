#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'

import sys
from mecoconfig import MECOConfiger
from mecodbconnect import MECODBConnector
import psycopg2

DEBUG = 1


class MECODBUtil(object):
    """
    Utility methods.
    """

    def __init__(self):
        """
        Constructor.
        """

        self.configer = MECOConfiger()

    def getLastSequenceID(self, conn, tableName, columnName):
        """
        Get last sequence ID value for the given sequence and for the
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

        row = None

        try:
            row = cur.fetchone()
        except psycopg2.ProgrammingError, e:
            print "Failed to retrieve the last sequence value."
            print "Exception is %s" % e
            sys.exit(-1)

        lastSequenceValue = row[0]

        if lastSequenceValue is None:
            print"Critical error. Last sequence value could not be retrieved."
            sys.exit(-1)

        return lastSequenceValue

    def executeSQL(self, cursor, sql):
        """
        Execute SQL given a cursor and a SQL statement.

        :param cursor: A database cursor.
        :param sql: A SQL statement.
        :returns: True for success, False for failure.
        """

        success = True
        try:
            cursor.execute(sql)
        except Exception, e:
            success = False
            print "SQL execute failed using %s." % sql
            print "The error is: ", e[0]
            print
            sys.exit(-1)
            # return False

        print "SQL execute was successful."

        return success

    def eraseTestMeco(self):
        """
        Erase the testing database. The name of the testing database is
        determined from the configuration file and must be set correctly.

        All sequences are reset to start with the value of one (1).
        """

        self.dbConnect = MECODBConnector(True)
        self.conn = self.dbConnect.connectDB()
        dbCursor = self.conn.cursor()

        databaseName = self.getDBName(dbCursor)[0]

        if (not (self.configer.configOptionValue("Database",
                                                 "testing_db_name") ==
                     databaseName)):
            print "Testing DB name doesn't match %s." % self.configer\
                .configOptionValue(
                "Database", "testing_db_name")
            exit(-1)

        print "Erasing testing database %s." % databaseName
        sql = ("""delete from "MeterData";""",
               """ALTER SEQUENCE interval_id_seq RESTART WITH 1;""",
               """ALTER SEQUENCE intervalreaddata_id_seq RESTART WITH 1;""",
               """ALTER SEQUENCE meterdata_id_seq RESTART WITH 1;""",
               """ALTER SEQUENCE reading_id_seq RESTART WITH 1;""",
               """ALTER SEQUENCE register_id_seq RESTART WITH 1;""",
               """ALTER SEQUENCE registerdata_id_seq RESTART WITH 1;""",
               """ALTER SEQUENCE registerread_id_seq RESTART WITH 1;""",
               """ALTER SEQUENCE tier_id_seq RESTART WITH 1;""",
               """ALTER SEQUENCE event_data_id_seq RESTART WITH 1;""",
               """ALTER SEQUENCE event_id_seq RESTART WITH 1;"""
        )

        for statement in sql:
            print "sql = %s" % statement
            self.executeSQL(dbCursor, statement)
            self.conn.commit()

        self.dbConnect.closeDB(self.conn)

    def getDBName(self, cursor):
        """
        :returns: Name of the current database.
        """

        self.executeSQL(cursor, "select current_database()")
        row = cursor.fetchone()
        return row[0]

