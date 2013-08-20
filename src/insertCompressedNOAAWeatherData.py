#!/usr/bin/env python -u
# -*- coding: utf-8 -*-

"""
Usage:

time python -u ${PATH}/insertCompressedNOAAWeatherData.py [--testing] [--email]

This script only supports processing of *hourly.txt.gz files.
"""

__author__ = 'Daniel Zhang (張道博)'

TESTING = False
KAHULUI_AIRPORT = '22516'

import os
import fnmatch
from msg_configer import MSGConfiger
from msg_notifier import MSGNotifier
import argparse
from msg_logger import MSGLogger
import gzip
from msg_noaa_weather_data_parser import MSGNOAAWeatherDataParser
from msg_noaa_weather_data_inserter import MSGNOAAWeatherDataInserter
from msg_db_connector import MSGDBConnector
from msg_time_util import MSGTimeUtil
from msg_noaa_weather_data_util import MSGWeatherDataUtil


configer = MSGConfiger()
logger = MSGLogger(__name__, 'info')
binPath = MSGConfiger.configOptionValue(configer, "Executable Paths",
                                        "bin_path")
commandLineArgs = None
msgBody = ''
notifier = MSGNotifier()
dataParser = MSGNOAAWeatherDataParser()
inserter = MSGNOAAWeatherDataInserter()

timeUtil = MSGTimeUtil()


def processCommandLineArguments():
    global argParser, commandLineArgs
    argParser = argparse.ArgumentParser(
        description = 'Perform recursive insertion of compressed weather data'
                      ' contained in the current directory to the MECO '
                      'database specified in the configuration file.')
    argParser.add_argument('--email', action = 'store_true', default = False,
                           help = 'Send email notification if this flag is '
                                  'specified.')
    argParser.add_argument('--testing', action = 'store_true', default = False,
                           help = 'If this flag is on, '
                                  'insert data to the testing database as '
                                  'specified in the local configuration file.')
    argParser.add_argument('--alldata', action = 'store_true', default = False,
                           help = 'If this flag is on, all weather data will '
                                  'be processed for insertion versus only '
                                  'processing the latest data. Processing '
                                  'only the latest data is the default '
                                  'behavior.')
    commandLineArgs = argParser.parse_args()


processCommandLineArguments()

if commandLineArgs.testing:
    logger.log("Testing mode is ON.\n", 'info')
    connector = MSGDBConnector(True)
else:
    connector = MSGDBConnector(testing = commandLineArgs.testing)
if commandLineArgs.email:
    logger.log("Email will be sent.\n", 'info')

conn = connector.conn

msg = ''
databaseName = ''

if commandLineArgs.testing:
    databaseName = configer.configOptionValue("Database", "testing_db_name")
else:
    databaseName = configer.configOptionValue("Database", "db_name")

msg = "Recursively inserting NOAA weather data to the database named %s." % \
      databaseName
print msg
msgBody += msg + "\n"

startingDirectory = os.getcwd()
msg = "Starting in %s." % startingDirectory
print msg
msgBody += msg + "\n"

allDays = []
weatherDays = []
setOfAllDays = set()
for root, dirnames, filenames in os.walk('.'):

    if commandLineArgs.alldata:
        # Load ALL data.
        for filename in fnmatch.filter(filenames, '*hourly.txt.gz'):
            fullPath = os.path.join(root, filename)
            msg = fullPath
            print msg
            msgBody += "Processing %s.\n" % msg
            fileObject = gzip.open(fullPath, "rb")
            weatherDays = inserter.insertDataDict(conn, 'WeatherNOAA',
                                                  dataParser.parseWeatherData(
                                                      fileObject,
                                                      [KAHULUI_AIRPORT]),
                                                  commit = True)
            allDays += weatherDays

            fileObject.close()
            if TESTING:
                break

    else: # Only process the latest data from the last loaded date.
        weatherUtil = MSGWeatherDataUtil()
        keepList = weatherUtil.getKeepList(weatherUtil.fileList,
                                           connector.conn.cursor())

        print "keep list = %s" % keepList

        keepDates = [weatherUtil.datePart(filename = k) for k in keepList]
        hourlyNames = [k + 'hourly.txt.gz' for k in keepDates]

        for n in hourlyNames:
            fullPath = os.path.join(root, n)
            msg = fullPath
            print msg
            msgBody += "Processing %s.\n" % msg
            fileObject = gzip.open(fullPath, "rb")
            weatherDays = inserter.insertDataDict(conn, 'WeatherNOAA',
                                                  dataParser.parseWeatherData(
                                                      fileObject,
                                                      [KAHULUI_AIRPORT]),
                                                  commit = True)
            allDays += weatherDays

            fileObject.close()
            if TESTING:
                break

if len(allDays) == 0:
    msgBody += "No weather data was processed."
else:
    setOfAllDays = set(allDays)
    msgBody += timeUtil.reportOfDays(setOfAllDays)

parseLog = ''

if commandLineArgs.email:
    notifier.sendMailWithAttachments(msgBody, files = None,
                                     testing = commandLineArgs.testing)
