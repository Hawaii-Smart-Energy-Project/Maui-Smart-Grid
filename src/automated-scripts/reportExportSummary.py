#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'
__copyright__ = 'Copyright (c) 2014, University of Hawaii Smart Energy Project'
__license__ = 'https://raw.github' \
              '.com/Hawaii-Smart-Energy-Project/Maui-Smart-Grid/master/BSD' \
              '-LICENSE.txt'

from msg_logger import MSGLogger
from msg_db_exporter import MSGDBExporter


class ExportSummaryReporter(object):
    def __init__(self):
        """
        Constructor.
        """
        self.logger = MSGLogger(__name__, 'DEBUG')
        self.exporter = MSGDBExporter()


    def sendCurrentExportSummary(self):
        """
        :return:
        """
        self.exporter.sendExportSummary(self.exporter.currentExportSummary())


if __name__ == '__main__':
    ExportSummaryReporter().sendCurrentExportSummary()
