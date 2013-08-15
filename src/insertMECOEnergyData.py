#!/usr/bin/env python -u
# -*- coding: utf-8 -*-

"""
Usage:

time python -u ${PATH}/insertMECOEnergyData.py > ${LOG_FILE}

From the *current directory*, recursively descend into every existing folder and
insert all data that is found.

This script makes use of insertSingleMECOEnergyDataFile.py.

This script only supports processing of *.xml.gz files.
"""

__author__ = 'Daniel Zhang (張道博)'
__copyright__ = 'Copyright (c) 2013, University of Hawaii Smart Energy Project'
__license__ = 'https://raw.github' \
              '.com/Hawaii-Smart-Energy-Project/Maui-Smart-Grid/master/BSD' \
              '-LICENSE.txt'

import os
import fnmatch
import sys
from subprocess import call
from msg_configer import MSGConfiger
import re
from msg_notifier import MSGNotifier
import argparse
from meco_plotting import MECOPlotting
from insertSingleMECOEnergyDataFile import Inserter
import time
from msg_logger import MSGLogger
import multiprocessing

xmlGzCount = 0
xmlCount = 0
configer = MSGConfiger()
logger = MSGLogger(__name__, 'info')
binPath = MSGConfiger.configOptionValue(configer, "Executable Paths",
                                        "bin_path")
commandLineArgs = None
global msgBody
msgBody = ''
notifier = MSGNotifier()

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


def makePlotAttachments():
    """
    Make data plots.
    """

    plotPath = configer.configOptionValue("Data Paths", "plot_path")
    sys.stderr.write("plotPath = %s\n" % plotPath)

    # If the plot doesn't exist then return.
    if not os.path.isdir(plotPath):
        return []

    attachments = ["%s/ReadingAndMeterCounts.png" % plotPath]
    for a in attachments:
        sys.stderr.write("attachment = %s\n" % a)
    return attachments


def logLegend():
    """
    Output a legend describing the concise report format.
    """

    legend = "Log Legend: {} = dupes, () = element group, " \
             "[] = process for insert elements, <> = <reading insert count, " \
             "register insert count, event insert count, group insert count," \
             "total insert count>, * = commit\nrd = reading, re = register, " \
             "ev = event"
    return legend


def insertDataWrapper(fullPath):
    """
    A wrapper for data insertion multiprocessing.
    :returns: Log of parsing along with performance results.
    """

    global msgBody
    logger.log('Inserting data.')
    logger.logAndWrite("current process is %s" % multiprocessing.current_process())

    pattern = 'Process-(\d+),'
    jobString = str(multiprocessing.current_process())
    print "jobstring = %s" % jobString
    match = re.search(pattern, jobString)
    assert match.group(1) is not None, "Process ID was matched."

    # print queue.

    myLog = ''
    myLog += "\n"
    myLog += fullPath
    # print msg
    myLog += "\n"
    startTime = time.time()
    myLog += inserter.insertData(fullPath, testing = commandLineArgs.testing,
                                 jobID = match.group(1))
    myLog += "\n"
    myLog += "\nWall time = {:.2f} seconds.\n".format(
        time.time() - startTime)

    logger.log('myLog = %s' % myLog)

    msgBody += myLog

    # return myLog


def worker():
    for item in iter(queue.get, None):
        insertDataWrapper(item)
        queue.task_done()
    queue.task_done()


processCommandLineArguments()

inserter = Inserter()

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

msg = "Recursively inserting data to the database named %s." % databaseName
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
    if (commandLineArgs.email):
        notifier.sendNotificationEmail(msgBody, commandLineArgs.testing)
    sys.exit(-1)

insertScript = "%s/insertSingleMECOEnergyDataFile.py" % binPath
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

startTime = 0

pathsToProcess = []
for root, dirnames, filenames in os.walk('.'):
    for filename in fnmatch.filter(filenames, '*.xml.gz'):
        if re.search('.*log\.xml', filename) is None: # Skip *log.xml files.
            xmlGzCount += 1
            pathsToProcess.append(os.path.join(root, filename))

            # Execute the insert data script for the file.

            # if USE_SCRIPT_METHOD:
            #     if commandLineArgs.testing:
            #         call([insertScript, "--testing", "--filepath", fullPath])
            # else:
            # The object method is preferred.
            # startTime = time.time()
            # parseLog = inserter.insertData(fullPath,
            #                                testing = commandLineArgs
            #                                .testing)
            # msgBody += parseLog + "\n"
            # msgBody += "\nWall time = {:.2f} seconds.\n".format(
            #     time.time() - startTime)
            # pass

try:
    pool = multiprocessing.Pool(
        int(configer.configOptionValue('Hardware', 'multiprocessing_limit')))

    # result = pool.map_async(insertDataWorker, pathsToProcess)
    # msgBody += result.get(999999)
    # print "result"
    # print "**************************************************************"
    # print result.get(999999)
    # result = pool.map(insertDataWorker, pathsToProcess)

    # logger.log('result = %s' % result)
    # pool.close()
    # pool.join()

    queue = multiprocessing.JoinableQueue()
    procs = []
    for i in range(
            int(configer.configOptionValue('Hardware',
                                           'multiprocessing_limit'))):
        procs.append(multiprocessing.Process(target = worker))
        procs[-1].daemon = True
        procs[-1].start()

    for path in pathsToProcess:
        queue.put(path)

    queue.join()

except Exception, e:
    logger.log('An exception occurred: %s' % e, 'error')

msgBody += "\n" + logLegend() + "\n"

msg = "\nProcessed file count is %s.\n" % xmlGzCount

print msg
msgBody += msg + "\n"

plotter = MECOPlotting(commandLineArgs.testing)

try:
    plotter.plotReadingAndMeterCounts(databaseName)
    msg = "\nPlot is attached.\n"
except:
    # @todo What exception is thrown?
    msg = "\nFailed to generate plot.\n"

msgBody += msg

if commandLineArgs.email:
    notifier.sendMailWithAttachments(msgBody, makePlotAttachments(),
                                     commandLineArgs.testing)

logger.log("msgBody = %s" % msgBody)
