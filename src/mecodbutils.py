#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'

import sys


class MECODBUtil(object) :
    """Utility methods.
    """

    def __init__(self) :
        """Constructor
        """

    def getLastSequenceID(self, conn, tableName, columnName) :
        """Get last sequence ID value for the given sequence and for the given connection.
        :rtype : object
        :param conn
        :param sequenceName
        :returns: last sequence value or None if not found
        """

        sql = "select currval(pg_get_serial_sequence('\"%s\"','%s'))" % (
        tableName, columnName)

        cur = conn.cursor()
        cur.execute(sql)
        row = cur.fetchone()
        lastSequenceValue = row[0]

        if lastSequenceValue is None :
            print"Critical error. Last sequence value could not be retrieved."
            sys.exit()

        return lastSequenceValue

    def executeSQL(self, cursor, sql):
        """Execute SQL given a cursor and a SQL statement.
        :cursor Database cursor
        :sql SQL statement
        :return True for success, False for failure
        """

        success = True
        try :
            cursor.execute(sql)
        except Exception, e :
            success = False
            print "execute failed with " + sql
            print "ERROR: ", e[0]
            print

        return success




