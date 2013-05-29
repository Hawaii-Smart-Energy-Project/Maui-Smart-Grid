#!/usr/bin/env python -u
# -*- coding: utf-8 -*-

"""
Usage:

time python -u ${PATH}/recursivelyInsertData.py > ${LOG_FILE}

From the current directory, recursively descend into every existing folder and
insert all data that is found.

This script makes use of insertData.py.

This script only supports processing of *.xml.gz files.
"""

__author__ = 'Daniel Zhang (張道博)'

import os
import fnmatch
import sys
from subprocess import call
from mecoconfig import MECOConfiger
import re
from meconotifier import MECONotifier
import argparse
from mecoplotting import MECOPlotting
from insertData import Inserter

xmlGzCount = 0
xmlCount = 0
configer = MECOConfiger()
binPath = MECOConfiger.configOptionValue(configer, "Executable Paths",
                                         "bin_path")
commandLineArgs = None
msgBody = ''
notifier = MECONotifier()

USE_SCRIPT_METHOD = False


def processCommandLineArguments():
    global parser, commandLineArgs
    parser = argparse.ArgumentParser(
        description = 'Perform recursive insertion of data contained in the '
                      'current directory to the MECO database specified in the '
                      'configuration file.')
    parser.add_argument('--email', action = 'store_true', default = False,
                        help = 'Send email notification if this flag is '
                               'specified.')
    parser.add_argument('--testing', action = 'store_true', default = False,
                        help = 'If this flag is on, '
                               'insert data to the testing database as '
                               'specified in the local configuration file.')
    commandLineArgs = parser.parse_args()


processCommandLineArguments()

inserter = Inserter()

if commandLineArgs.testing:
    sys.stderr.write("Testing mode is ON.\n")
if commandLineArgs.email:
    sys.stderr.write("Email will be sent.\n")

msg = ''
if commandLineArgs.testing:
    msg = "Recursively inserting data to the database named %s." % configer \
        .configOptionValue("Database", "testing_db_name")
else:
    msg = "Recursively inserting data to the database named %s." % configer \
        .configOptionValue("Database", "db_name")

print msg
msgBody += msg + "\n"

startingDirectory = os.getcwd()
msg = "Starting in %s." % startingDirectory
print msg
msgBody += msg + "\n"

for root, dirnames, filenames in os.walk('.'):

    for filename in fnmatch.filter(filenames, '*.xml'):
        fullPath = os.path.join(root, filename)
        msg = fullPath
        print msg
        msgBody += msg + "\n"
        xmlCount += 1

if xmlCount != 0:
    msg = "Found XML files that are not gzip compressed.\nUnable to proceed."
    print msg
    msgBody += msg + "\n"
    notifier.sendNotificationEmail(msgBody)
    sys.exit(-1)

insertScript = "%s/insertData.py" % binPath
msg = "insertScript = %s" % insertScript
print msg
msgBody += msg + "\n"

parseLog = ''

try:
    with open(insertScript):
        pass
except IOError:
    msg = "Insert script %s not found." % insertScript
    print msg
    msgBody += msg + "\n"

for root, dirnames, filenames in os.walk('.'):
    for filename in fnmatch.filter(filenames, '*.xml.gz'):
        if re.search('.*log\.xml', filename) is None: # skip *log.xml files

            fullPath = os.path.join(root, filename)
            msg = fullPath
            print msg
            msgBody += msg + "\n"
            xmlGzCount += 1

            # Execute the insert data script for the file.

            if USE_SCRIPT_METHOD:
                if commandLineArgs.testing:
                    call([insertScript, "--testing", "--filepath", fullPath])
                else:
                    call([insertScript, "--filepath", fullPath])
            else:
                # Object method is preferred.
                parseLog = inserter.insertData(fullPath, commandLineArgs.testing)
                msgBody += parseLog + "\n"

msg = "\n%s files were processed." % xmlGzCount
print msg
msgBody += msg + "\n"

plotter = MECOPlotting()
plotter.plotReadingAndMeterCounts()

if commandLineArgs.email:
    # notifier.sendNotificationEmail(msgBody)
    plotPath = configer.configOptionValue("Data Paths", "plot_path")
    notifier.sendMailWithAttachments(msgBody,
                                     ["%s/ReadingAndMeterCounts.png" % plotPath])
