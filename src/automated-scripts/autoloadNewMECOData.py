#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Check for new MECO data and load it if it is present.

This script is intended to be run automatically.
"""


__author__ = 'Daniel Zhang (張道博)'
__copyright__ = 'Copyright (c) 2013, University of Hawaii Smart Energy Project'
__license__ = 'https://raw.github' \
              '.com/Hawaii-Smart-Energy-Project/Maui-Smart-Grid/master/BSD' \
              '-LICENSE.txt'


from sek.logger import SEKLogger
from meco_data_autoloader import MECODataAutoloader

SUPPRESS_OUTPUT_FOR_NO_DATA = True

logger = SEKLogger(__name__)
autoloader = MECODataAutoloader()

if autoloader.newDataExists():
    logger.log('Loading new data.')
    autoloader.loadNewData()
    logger.log('Archiving loaded data.')
    autoloader.archiveLoadedData()
else:
    if not SUPPRESS_OUTPUT_FOR_NO_DATA:
        logger.log('No new data was found.')
