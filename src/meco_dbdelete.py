#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'

import psycopg2
import psycopg2.extras
from mecodbutils import MECODBUtil

class MECODBDeleter(object) :
    """Provide delete routines for MECO DB.
    """

    def __init__(self) :
        """Constructor
        """
        self.dbUtil = MECODBUtil()

    def deleteRecord(self, conn, tableName, idText, idValue) :
        """Delete record from DB where record has an int-based serial number.
        param: tableName
        param: idText DB column name for record ID
        param: idValue Value of the ID to be deleted
        """
        sql = "delete from \"%s\" where %s = %s" % (tableName, idText, idValue)
        dictCur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
        self.dbUtil.executeSQL(dictCur, sql)
        conn.commit()
