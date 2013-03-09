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


