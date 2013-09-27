#!/usr/bin/env python -u
# -*- coding: utf-8 -*-

"""
Usage:

time python -u ${PATH}/insertMECOEnergyData.py > ${LOG_FILE}

From the *current working directory*, recursively descend into every existing
folder and
insert all data that is found using multiprocessing.

This script makes use of insertSingleMECOEnergyDataFile.py.

This script only supports processing of gzip-compressed XML (*.xml.gz) files.
"""

__author__ = 'Daniel Zhang (張道博)'
__copyright__ = 'Copyright (c) 2013, University of Hawaii Smart Energy Project'
__license__ = 'https://raw.github' \
              '.com/Hawaii-Smart-Energy-Project/Maui-Smart-Grid/master/BSD' \
              '-LICENSE.txt'

import os
import fnmatch
import sys
#from subprocess import call
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

#USE_SCRIPT_METHOD = False


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

    :returns: List of attachments.
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

    :returns: String containing the legend.
    """

    legend = "Log Legend: #: = process ID, {} = dupes, () = element group, " \
             "[] = process for insert elements,\n"
    legend += "    <> = <reading insert count, register insert count, " \
              "event insert count, group insert count, total insert count>.\n"
    legend += "Final summary after (---): <> = <reading insert count, " \
              "register insert count, event insert count, total insert count>" \
              ".\n"
    legend += "Symbols: * = commit, rd = reading, re = register, ev = event.\n"
    return legend


def insertDataWrapper(fullPath):
    """
    A wrapper for data insertion multiprocessing.

    :param fullPath: Path of data to be processed.
    :returns: Log of parsing along with performance results.
    """

    pattern = 'Process-(\d+),'
    jobString = str(multiprocessing.current_process())
    match = re.search(pattern, jobString)
    assert match.group(1) is not None, "Process ID was matched."

    myLog = ''
    myLog += "\n"
    myLog += fullPath
    myLog += "\n"
    startTime = time.time()
    myLog += inserter.insertData(fullPath, testing = commandLineArgs.testing,
                                 jobID = match.group(1))
    myLog += "\n"
    myLog += "\nWall time = {:.2f} seconds.\n".format(time.time() - startTime)

    logger.log('myLog = %s' % myLog)

    return myLog


def worker(path, returnDict):
    """
    :param path
    :param returnDict
    """

    result = insertDataWrapper(path)
    pattern = 'Process-(\d+),'
    jobString = str(multiprocessing.current_process())
    match = re.search(pattern, jobString)
    assert match.group(1) is not None, "Process ID was matched."
    returnDict[match.group(1)] = result


if __name__ == '__main__':

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

    try:
        procs = []
        manager = multiprocessing.Manager()
        returnDict = manager.dict()

        for path in pathsToProcess:
            procs.append(
                multiprocessing.Process(target = worker, args = (path, returnDict)))
            procs[-1].daemon = True
            procs[-1].start()

        for proc in procs:
            proc.join()

        for key in returnDict.keys():
            sys.stderr.write("Process %s results:\n" % key)
            sys.stderr.write(returnDict[key])
            sys.stderr.write("\n")
            msgBody += returnDict[key]

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
    except Exception, e:
        msg = "\nFailed to generate plot.\n"
        logger.log('An exception occurred: Failed to generate plot. %s' % e,
                   'error')

    msgBody += msg

    if commandLineArgs.email:
        notifier.sendMailWithAttachments(msgBody, makePlotAttachments(),
                                         commandLineArgs.testing)

    logger.log("msgBody = %s" % msgBody)
