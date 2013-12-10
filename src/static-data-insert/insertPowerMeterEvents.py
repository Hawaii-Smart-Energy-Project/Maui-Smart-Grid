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
import datetime

cols = ['dtype', 'id', 'event_category', 'el_epoch_num', 'el_seq_num',
        'event_ack_status', 'event_text', 'event_time', 'generic_col_1',
        'generic_col_10', 'generic_col_2', 'generic_col_3', 'generic_col_4',
        'generic_col_5', 'generic_col_6', 'generic_col_7', 'generic_col_8',
        'generic_col_9', 'insert_ts', 'job_id', 'event_key', 'nic_reboot_count',
        'seconds_since_reboot', 'event_severity', 'source_id', 'update_ts',
        'updated_by_user', 'event_ack_note']


def extractTimestamp(timeString):
    ts = ''
    pattern = '(\d+)-(\w+)-(\d+)\s(\d+)\.(\d+)\.(\d+)\.(\d+)\s(\w+)'
    matches = re.search(pattern, timeString)

    tString = '%s-%s-%s %s.%s.%s.%s %s' % (
        matches.group(1), matches.group(2), matches.group(3), matches.group(4),
        matches.group(5), matches.group(6), matches.group(7)[:6],
        matches.group(8))

    #print matches.group(1)
    #print matches.group(2)
    #print matches.group(3)

    #print datetime.datetime.strptime(timeString, '%d-%b-%y %I.%M.%S.%f %p')

    #print tString

    return datetime.datetime.strptime(tString, '%d-%b-%y %I.%M.%S.%f %p')


def insertData(table, row, cols):
    global dbUtil
    global cursor

    vals = []
    i = 0
    for cell in row:
        val = cell.value

        # Handle setting of type.
        if cols[i] == 'id' or cols[i] == 'event_category' or cols[
            i] == 'event_key' or cols[i] == 'source_id':
            val = int(val)
        if cols[i] == 'event_time' or cols[i] == 'insert_ts' or cols[
            i] == 'update_ts':
            val = extractTimestamp(val)

        if val == '':
            val = 'NULL'
        else:
            val = """'%s'""" % val

        vals.append(val)
        i += 1

    #print 'cols: %s' % cols
    #print 'vals: %s' % vals

    sql = """INSERT INTO "%s" (%s) VALUES (%s)""" % (
        table, ','.join(cols), ','.join(vals))

    #print sql
    #for col in cols:
    #    i += 1
    dbUtil.executeSQL(cursor, sql)


connector = MSGDBConnector()
conn = connector.connectDB()
dbUtil = MSGDBUtil()
cursor = conn.cursor()
logger = MSGLogger(__name__)

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

#cols = dbUtil.tableColumns(cursor, table)

print cols

cnt = 0
workbookCount = 0

#newCols = []
#for col in cols:
#    Extract col from tuple.
#newCols.append(col[0])
#cols = newCols

for path in paths:
    workbookCount += 1
    logger.log('workbook: %s' % path)
    wb = xlrd.open_workbook(path)
    wb.sheet_names()
    print wb.sheet_names()
    sh = wb.sheet_by_index(0)
    print sh

    numRows = sh.nrows - 1

    currentRow = -1

    while currentRow < numRows:
        currentRow += 1
        row = sh.row(currentRow)

        # Row is a dict of the col vals.
        if currentRow != 0:
            insertData(table, row, cols)

    conn.commit()

logger.log('Workbook count: %d' % workbookCount)

exit(0)

