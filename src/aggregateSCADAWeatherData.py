#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Generates aggregated (average) SCADA weather data for 15-min intervals starting
at minute zero.

Provides intervals where the timestamp represents the end of the interval.

Usage:

    python aggregateSCADAWeatherData.py --startDate "${YYYY-MM-DD hh:mm:ss}"
                                        --endDate "${YYYY-MM-DD hh:mm:ss}"

Output is comma-separated data to STDOUT.

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
from msg_math_util import MSGMathUtil

NEXT_MINUTE_CROSSING = 0


def processCommandLineArguments():
    """
    Create command line arguments and parse them.
    """

    global parser, commandLineArgs
    parser = argparse.ArgumentParser(description = '')
    parser.add_argument('--startDate', type = str, required = True,
                        help = 'Start date of data to be evaluated.')
    parser.add_argument('--endDate', type = str, required = True,
                        help = 'End date of data to be evaluated.')
    commandLineArgs = parser.parse_args()


def emitAverage(timestamp, sum, cnt):
    tAvg = 'NULL'
    hAvg = 'NULL'
    if cnt[0] != 0:
        tAvg = sum[0] / cnt[0]
    if cnt[1] != 0:
        hAvg = sum[1] / cnt[1]

    print '%s, %s, %s' % (timestamp, tAvg, hAvg)


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


processCommandLineArguments()

logger = MSGLogger(__name__, 'INFO')
connector = MSGDBConnector()
conn = connector.connectDB()
dbUtil = MSGDBUtil()
mUtil = MSGMathUtil()

sql = """SELECT timestamp, met_air_temp_degf, met_rel_humid_pct
         FROM "KiheiSCADATemperatureHumidity"
         WHERE timestamp BETWEEN '%s' AND '%s'
         ORDER BY timestamp""" % (
    commandLineArgs.startDate, commandLineArgs.endDate)

cursor = conn.cursor()
dbUtil.executeSQL(cursor, sql)

rows = cursor.fetchall()

rowCnt = 0

sum = []
cnt = []
for i in range(2):
    sum.append(0)
    cnt.append(0)

for row in rows:

    if mUtil.isNumber(row[1]):
        sum[0] += row[1]
        cnt[0] += 1
    if mUtil.isNumber(row[2]):
        sum[1] += row[2]
        cnt[1] += 1

    minute = row[0].timetuple()[4]

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
        emitAverage(row[0], sum, cnt)
        sum = []
        cnt = []
        for i in range(2):
            sum.append(0)
            cnt.append(0)

    rowCnt += 1
