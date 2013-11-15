#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Generates aggregated (average) irradiance data for 15-min intervals starting at
minute zero.
"""

__author__ = 'Daniel Zhang (張道博)'
__copyright__ = 'Copyright (c) 2013, University of Hawaii Smart Energy Project'
__license__ = 'https://raw.github' \
              '.com/Hawaii-Smart-Energy-Project/Maui-Smart-Grid/master/BSD' \
              '-LICENSE.txt'

from msg_db_connector import MSGDBConnector
from msg_logger import MSGLogger
from msg_db_util import MSGDBUtil
import argparse

NEXT_MINUTE_CROSSING = 0


def processCommandLineArguments():
    """
    Create command line arguments and parse them.
    """

    global parser, commandLineArgs
    parser = argparse.ArgumentParser(description = '')
    parser.add_argument('--startDate', type = str)
    parser.add_argument('--endDate', type = str)
    commandLineArgs = parser.parse_args()


def emitAverage(sum, cnt, timestamp):
    myCount = 0
    idx = 0
    for item in sum:
        myCount += 1
        if cnt[idx] != 0:
            print '%s, %s, %s' % (myCount, timestamp, item / cnt[idx])
        else:
            print '%s, %s, %s' % (myCount, timestamp, 'NULL')
        idx += 1


def intervalCrossed(minute):
    global NEXT_MINUTE_CROSSING
    global logger

    if minute >= NEXT_MINUTE_CROSSING and minute <= 60 and \
                    NEXT_MINUTE_CROSSING != 0:
        logger.log('minute: %s, crossing: %s' % (minute, NEXT_MINUTE_CROSSING),
                   'DEBUG')

        NEXT_MINUTE_CROSSING += 15
        if NEXT_MINUTE_CROSSING >= 60:
            NEXT_MINUTE_CROSSING = 0
        return True

    elif NEXT_MINUTE_CROSSING == 0 and minute >= 0 and minute <= 15:
        logger.log('minute: %s, crossing: %s' % (minute, NEXT_MINUTE_CROSSING),
                   'DEBUG')

        NEXT_MINUTE_CROSSING = 15
        return True

    return False


def isNumber(s):
    try:
        float(s)
        return True
    except (TypeError, ValueError):
        return False


processCommandLineArguments()

logger = MSGLogger(__name__, 'INFO')
connector = MSGDBConnector()
conn = connector.connectDB()
dbUtil = MSGDBUtil()

sql = """SELECT sensor_id, irradiance_w_per_m2, timestamp FROM
"IrradianceData" where timestamp BETWEEN '%s' AND '%s'""" % (
    commandLineArgs.startDate, commandLineArgs.endDate)

cursor = conn.cursor()
dbUtil.executeSQL(cursor, sql)

rows = cursor.fetchall()
sum = list()

for i in range(4):
    sum.append(list())
    sum[i] = 0

cnt = list()
for i in range(4):
    cnt.append(list())
    cnt[i] = 0

rowCnt = 0
finalTimestamp = None

for row in rows:

    if isNumber(row[1]):
        cnt[row[0] - 1] += 1
        sum[row[0] - 1] += row[1]

    minute = row[2].timetuple()[4]
    finalTimestamp = row[2]

    if rowCnt == 0:
        if minute < 15:
            NEXT_MINUTE_CROSSING = 15
        elif minute < 30:
            NEXT_MINUTE_CROSSING = 30
        elif minute < 45:
            NEXT_MINUTE_CROSSING = 45
        else:
            NEXT_MINUTE_CROSSING = 0

    if (intervalCrossed(minute)):
        emitAverage(sum, cnt, row[2])
        cnt = 0
        sum = list()
        for i in range(4):
            sum.append(list())
            sum[i] = 0
        cnt = list()
        for i in range(4):
            cnt.append(list())
            cnt[i] = 0

    rowCnt += 1

# Handle end case.
emitAverage(sum, cnt, finalTimestamp)
