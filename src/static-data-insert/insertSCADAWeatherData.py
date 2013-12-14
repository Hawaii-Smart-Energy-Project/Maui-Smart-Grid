#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script for inserting Kihei SCADA temperature and humidity data.

Usage:

With the current working directory set to the path containing the data files,

    python insertSCADAWeatherData.py

"""

__author__ = 'Daniel Zhang (張道博)'
__copyright__ = 'Copyright (c) 2013, University of Hawaii Smart Energy Project'
__license__ = 'https://raw.github' \
              '.com/Hawaii-Smart-Energy-Project/Maui-Smart-Grid/master/BSD' \
              '-LICENSE.txt'

from msg_db_connector import MSGDBConnector
from msg_db_util import MSGDBUtil
import csv
import re

if __name__ == '__main__':

    connector = MSGDBConnector()
    conn = connector.connectDB()
    dbUtil = MSGDBUtil()
    cursor = conn.cursor()

    tFiles = ['Kihei AirTemp F 2013_07.csv', 'Kihei AirTemp F 2013_08.csv',
              'Kihei AirTemp F 2013_09.csv', 'Kihei AirTemp F 2013_10.csv']

    hFiles = ['Kihei_Rel_Humid 2013_07.csv', 'Kihei_Rel_Humid 2013_08.csv',
              'Kihei_Rel_Humid 2013_09.csv', 'Kihei_Rel_Humid 2013_10.csv']

    table = 'KiheiSCADATemperatureHumidity'
    tCols = ['timestamp', 'met_air_temp_degf']
    hCols = ['met_rel_humid_pct']

    cnt = 0

    temps = []
    t_i = 0
    h_i = 0

    for i in range(4):

        with open(tFiles[i], 'rb') as csvfile:
            print "Reading %s" % (tFiles[i])

            myReader = csv.reader(csvfile, delimiter = ',')

            for row in myReader:
                if cnt == 0:
                    cnt += 1
                    continue
                    #temps[t_i] = [row[0], row[1]]

                row[0] = row[0].replace('GMT-1000', '')
                row[0] = re.sub(r'\s24:', '\s00:', row[0])

                if row[1] == '':
                    row[1] = 'NULL'

                sql = """INSERT INTO "%s" (%s) VALUES (TIMESTAMP %s,%s)""" % (
                    table, ','.join(tCols), "'" + row[0].strip() + "'",
                    "'" + row[1].strip() + "'")

                sql = sql.replace("'NULL'", 'NULL')

                #print sql
                dbUtil.executeSQL(cursor, sql)

                cnt += 1
                if cnt % 10000 == 0:
                    conn.commit()

        conn.commit()
        cnt = 0

        with open(hFiles[i], 'rb') as csvfile:
            print "Reading %s" % (hFiles[i])

            myReader = csv.reader(csvfile, delimiter = ',')

            for row in myReader:
                if cnt == 0:
                    cnt += 1
                    continue

                row[0] = row[0].replace('GMT-1000', '')
                row[0] = re.sub(r'\s24:', '\s00:', row[0])

                if row[1] == '':
                    row[1] = 'NULL'

                sql = """UPDATE "%s" SET %s = %s WHERE timestamp =
                TIMESTAMP '%s'""" % (
                    table, ','.join(hCols), "'" + row[1].strip() + "'",
                    row[0].strip())

                sql = sql.replace("'NULL'", 'NULL')

                #print sql
                dbUtil.executeSQL(cursor, sql)

                cnt += 1
                if cnt % 10000 == 0:
                    conn.commit()
                    pass

        conn.commit()
        cnt = 0
