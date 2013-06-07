#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Preprocess weather data from Kahalui weather stations and insert to the
data store.
"""

__author__ = 'Daniel Zhang (張道博)'

import csv
import sys
import re
from mecodbconnect import MECODBConnector
from mecodbutils import MECODBUtil
from meconotifier import MECONotifier
from mecoconfig import MECOConfiger

try:
    len(sys.argv[1])
except:
    print "Usage: insertWeatherData.py FILENAME"
    sys.exit()

filename = sys.argv[1]
msgBody = ''

connector = MECODBConnector()
conn = connector.connectDB()
cur = conn.cursor()
dbUtil = MECODBUtil()
notifier = MECONotifier()
sqlSuccess = False
configer = MECOConfiger()

dbName = configer.configOptionValue("Database", "db_name")

msg = ("Loading weather data in file %s to database %s.\n" % (
    filename, dbName))
sys.stderr.write(msg)
msgBody += msg

cols = ["wban", "datetime", "station_type", "sky_condition",
        "sky_condition_flag", "visibility", "visibility_flag", "weather_type",
        "weather_type_flag", "dry_bulb_farenheit", "dry_bulb_farenheit_flag",
        "dry_bulb_celsius", "dry_bulb_celsius_flag", "wet_bulb_farenheit",
        "wet_bulb_farenheit_flag", "wet_bulb_celsius", "wet_bulb_celsius_flag",
        "dew_point_farenheit", "dew_point_farenheit_flag", "dew_point_celsius",
        "dew_point_celsius_flag", "relative_humidity", "relative_humidity_flag",
        "wind_speed", "wind_speed_flag", "wind_direction",
        "wind_direction_flag", "value_for_wind_character",
        "value_for_wind_character_flag", "station_pressure",
        "station_pressure_flag", "pressure_tendency", "pressure_tendency_flag",
        "pressure_change", "pressure_change_flag", "sea_level_pressure",
        "sea_level_pressure_flag", "record_type", "record_type_flag",
        "hourly_precip", "hourly_precip_flag", "altimeter", "altimeter_flag"]

myFile = open(filename, "r")
reader = csv.reader(myFile)
rowNum = 0
lastCol = 0
for row in reader:
    data = []
    newDate = ''

    # Handle the header row.
    if rowNum == 7:
        colNum = 0
        for col in row:
            colNum += 1
        lastCol = colNum

    # Skip 7 lines of header.
    if rowNum < 8:
        pass

    else:
        colNum = 0
        for col in row:

            if colNum == 1: # date column
                newDate = '%s' % (
                    (col[0:4]) + '-%s' % (col[4:6]) + '-%s' % (col[6:8]))

            elif colNum == 2: # time column
                time = col.zfill(4)
                data.append('%s %s:%s' % (newDate, time[0:2], time[2:4]))
                newDate = ''
            else:
                data.append('%s' % col)
            colNum += 1

        if colNum == lastCol:
            for i in range(0, lastCol - 1):

                try:
                    if len(data[i]) == 0 or len(
                            re.sub("\s+", "", data[i])) == 0:
                        data[i] = 'NULL'
                    else:
                        data[i] = "'" + data[i] + "'"
                except IndexError, e:
                    assert data != [], "Data should never be empty."

            sql = """INSERT INTO "WeatherKahaluiAirport" (%s) VALUES (%s)""" % (
                ','.join(cols), ','.join(data[0:lastCol - 1]))
            print "sql = %s" % sql
            sqlSuccess = dbUtil.executeSQL(cur, sql)

    rowNum += 1

myFile.close()
conn.commit()

if sqlSuccess:
    msg = "SQL operation was successful.\n"
    sys.stderr.write(msg)
    msgBody += msg
else:
    msg = "SQL operation was NOT successful.\n"
    sys.stderr.write(msg)
    msgBody += msg

notifier.sendNotificationEmail(msgBody)
