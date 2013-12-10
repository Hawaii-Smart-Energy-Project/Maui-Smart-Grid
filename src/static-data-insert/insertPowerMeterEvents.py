#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script for inserting Power Meter Events directly from MS Excel source data.

Usage:

With the current working directory set to the path containing the data files:

    python insertPowerMeterEvents.py

"""

__author__ = 'Daniel Zhang (張道博)'
__copyright__ = 'Copyright (c) 2013, University of Hawaii Smart Energy Project'
__license__ = 'https://raw.github' \
              '.com/Hawaii-Smart-Energy-Project/Maui-Smart-Grid/master/BSD' \
              '-LICENSE.txt'

from msg_db_connector import MSGDBConnector
from msg_db_util import MSGDBUtil
import re
import os
import fnmatch
import xlrd
from msg_logger import MSGLogger


def getColumns(cursor, table):
    """
    :returns: List of tuples with column names in the first position.
    """

    global dbUtil
    sql = """select column_name from information_schema.columns where
    table_name='%s';""" % table
    print sql
    dbUtil.executeSQL(cursor, sql)

    return cursor.fetchall() # Each column is an n-tuple.


connector = MSGDBConnector()
conn = connector.connectDB()
dbUtil = MSGDBUtil()
cursor = conn.cursor()
logger = MSGLogger(__name__)

files = []
paths = []
patterns = ['*.xlsx']
matchCnt = 0
for root, dirs, filenames in os.walk('.'):
    for pat in patterns:
        for filename in fnmatch.filter(filenames, pat):
            paths.append(os.path.join(root, filename))
            matchCnt += 1

print "paths = %s" % paths

table = 'PowerMeterEvents'

cols = getColumns(cursor, table)

print cols

cnt = 0
workbookCount = 0

for path in paths:
    workbookCount += 1
    logger.log('workbook: %s' % path)
    wb = xlrd.open_workbook(path)
    wb.sheet_names()
    print wb.sheet_names()
    sh = wb.sheet_by_index(0)
    print sh

    num_rows = sh.nrows - 1

    curr_row = -1

    while curr_row < num_rows:
        curr_row += 1
        try:
            row = sh.row(curr_row)
        except (xlrd.biffh.XLRDError, e):
            # Ignore unsupported format error.
            pass



        # Row is a dict of the col vals.
        #print row


logger.log('Workbook count: %d' % workbookCount)



exit(0)

