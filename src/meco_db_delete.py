#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'
__copyright__ = 'Copyright (c) 2014, University of Hawaii Smart Energy Project'
__license__ = 'https://raw.github' \
              '.com/Hawaii-Smart-Energy-Project/Maui-Smart-Grid/master/BSD' \
              '-LICENSE.txt'

import psycopg2
import psycopg2.extras
from msg_db_util import MSGDBUtil


class MECODBDeleter(object):
    """
    Provide delete routines for MECO DB.
    """

    def __init__(self):
        """
        Constructor.
        """
        self.dbUtil = MSGDBUtil()


    def deleteRecord(self, conn, tableName, idText, idValue):
        """
        Delete record from DB where record has an int-based serial number.

        param: tableName
        param: idText DB column name for record ID
        param: idValue Value of the ID to be deleted
        """

        sql = """DELETE FROM "{}" where {} = {}""".format(tableName, idText,
                                                          idValue)
        dictCur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
        self.dbUtil.executeSQL(dictCur, sql)
        conn.commit()
