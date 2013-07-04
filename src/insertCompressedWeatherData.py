#!/usr/bin/env python -u
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'

"""
Usage:

time python -u ${PATH}/insertCompressedWeatherData.py [--testing] [--email]

This script only supports processing of *hourly.txt.gz files.
"""

import os
import fnmatch
from mecoconfig import MECOConfiger
from meconotifier import MECONotifier
import argparse
from mecologger import MECOLogger
import gzip

configer = MECOConfiger()
logger = MECOLogger(__name__, 'info')
binPath = MECOConfiger.configOptionValue(configer, "Executable Paths",
                                         "bin_path")
commandLineArgs = None
msgBody = ''
notifier = MECONotifier()


def processCommandLineArguments():
    global parser, commandLineArgs
    parser = argparse.ArgumentParser(
        description = 'Perform recursive insertion of compressed weather data'
                      ' contained in the current directory to the MECO '
                      'database specified in the configuration file.')
    parser.add_argument('--email', action = 'store_true', default = False,
                        help = 'Send email notification if this flag is '
                               'specified.')
    parser.add_argument('--testing', action = 'store_true', default = False,
                        help = 'If this flag is on, '
                               'insert data to the testing database as '
                               'specified in the local configuration file.')
    commandLineArgs = parser.parse_args()


processCommandLineArguments()

if commandLineArgs.testing:
    logger.log("Testing mode is ON.\n", 'info')
if commandLineArgs.email:
    logger.log("Email will be sent.\n", 'info')

msg = ''
databaseName = ''

if commandLineArgs.testing:
    databaseName = configer.configOptionValue("Database", "testing_db_name")
else:
    databaseName = configer.configOptionValue("Database", "db_name")

msg = "Recursively inserting weather data to the database named %s." % \
      databaseName
print msg
msgBody += msg + "\n"

startingDirectory = os.getcwd()
msg = "Starting in %s." % startingDirectory
print msg
msgBody += msg + "\n"

for root, dirnames, filenames in os.walk('.'):

    for filename in fnmatch.filter(filenames, '*hourly.txt.gz'):
        fullPath = os.path.join(root, filename)
        msg = fullPath
        print msg
        fileObject = gzip.open(fullPath, "rb")


parseLog = ''

if commandLineArgs.email:
    # notifier.sendMailWithAttachments(msgBody, makePlotAttachments(),
    #                                  commandLineArgs.testing)
    pass
