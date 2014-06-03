#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Grab the list of databases to be exported in the MSG configuration file and
export them to cloud storage.

Files beyond a maximum limit are split according to the number of chunks set
in the config file.

Usage:

    python exportDBsToCloud.py

"""

__author__ = 'Daniel Zhang (張道博)'
__copyright__ = 'Copyright (c) 2014, University of Hawaii Smart Energy Project'
__license__ = 'https://raw.github' \
              '.com/Hawaii-Smart-Energy-Project/Maui-Smart-Grid/master/BSD' \
              '-LICENSE.txt'

from msg_logger import MSGLogger
from msg_notifier import MSGNotifier
from msg_db_exporter import MSGDBExporter
import argparse
import time


COMMAND_LINE_ARGS = None


def processCommandLineArguments():
    """
    Generate command-line arguments. Load them into global variable
    COMMAND_LINE_ARGS.
    """

    global COMMAND_LINE_ARGS
    parser = argparse.ArgumentParser(description = '')
    parser.add_argument('--dbname', help = 'Database file to be uploaded.')
    parser.add_argument('--fullpath',
                        help = 'Full path to database file to be uploaded.')
    parser.add_argument('--testing', action = 'store_true', default = False)

    COMMAND_LINE_ARGS = parser.parse_args()


if __name__ == '__main__':
    logger = MSGLogger(__name__, 'INFO')

    logger.log("Exporting DBs to cloud.")
    processCommandLineArguments()

    exporter = MSGDBExporter()
    notifier = MSGNotifier()
    exporter.logger.shouldRecord = True

    startTime = time.time()
    noErrors = exporter.exportDB(
        databases = exporter.configer.configOptionValue('Export',
                                                        'dbs_to_export').split(
            ','), toCloud = True, testing = COMMAND_LINE_ARGS.testing,
        numChunks = int(exporter.configer.configOptionValue('Export',
                                                            'num_split_sections')),
        deleteOutdated = True)

    wallTime = time.time() - startTime
    wallTimeMin = int(wallTime / 60.0)
    wallTimeSec = (wallTime - wallTimeMin * 60.0)

    if noErrors:
        exporter.logger.log('No errors occurred during export.', 'info')
    else:
        exporter.logger.log('ERRORS occurred during export.', 'warning')

    exporter.logger.log('Free space remaining: %d' % exporter.freeSpace(),
                        'info')

    exporter.logger.log(
        'Wall time: {:d} min {:.2f} s.'.format(wallTimeMin, wallTimeSec),
        'info')

    # Send the available file list by POST.
    exporter.sendDownloadableFiles()

    # Testing recording log output.
    myPath = '{}/{}'.format(exporter.exportTempWorkPath, 'export-report.txt')
    fp = open(myPath, 'wb')
    fp.write(exporter.logger.recording)
    fp.close()
