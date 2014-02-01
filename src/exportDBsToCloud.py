#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Usage:

    python exportDBsToCloud.py

"""

__author__ = 'Daniel Zhang (張道博)'
__copyright__ = 'Copyright (c) 2013, University of Hawaii Smart Energy Project'
__license__ = 'https://raw.github' \
              '.com/Hawaii-Smart-Energy-Project/Maui-Smart-Grid/master/BSD' \
              '-LICENSE.txt'

from msg_logger import MSGLogger
from msg_notifier import MSGNotifier
from msg_db_exporter import MSGDBExporter
import argparse
import time


commandLineArgs = None


def processCommandLineArguments():
    """
    Generate command-line arguments. Load them into global variable
    commandLineArgs.
    """

    global parser, commandLineArgs
    parser = argparse.ArgumentParser(description = '')
    parser.add_argument('--dbname', help = 'Database file to be uploaded.')
    parser.add_argument('--fullpath',
                        help = 'Full path to database file to be uploaded.')
    parser.add_argument('--testing', action = 'store_true', default = False)

    commandLineArgs = parser.parse_args()


if __name__ == '__main__':
    logger = MSGLogger(__name__, 'INFO')

    logger.log("Exporting DBs to cloud.")
    processCommandLineArguments()

    exporter = MSGDBExporter()
    notifier = MSGNotifier()
    exporter.logger.shouldRecord = True

    startTime = time.time()
    exporter.exportDB(databases = exporter.configer.configOptionValue('Export',
                                                                      'dbs_to_export').split(
        ','), toCloud = True, testing = commandLineArgs.testing, numChunks = 4)
    wallTime = time.time() - startTime
    wallTimeMin = int(wallTime / 60.0)
    wallTimeSec = (wallTime - wallTimeMin * 60.0)

    exporter.logger.log('Free space remaining: %d' % exporter.freeSpace(),
                        'info')

    exporter.logger.log(
        'Wall time: {:d} min {:.2f} s.'.format(wallTimeMin, wallTimeSec),
        'info')
