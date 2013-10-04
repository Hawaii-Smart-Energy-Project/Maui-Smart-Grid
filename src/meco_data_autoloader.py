#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'
__copyright__ = 'Copyright (c) 2013, University of Hawaii Smart Energy Project'
__license__ = 'https://raw.github' \
              '.com/Hawaii-Smart-Energy-Project/Maui-Smart-Grid/master/BSD' \
              '-LICENSE.txt'

from msg_logger import MSGLogger
from msg_configer import MSGConfiger
import os
import fnmatch
from msg_file_util import MSGFileUtil
import subprocess
import os

class MECODataAutoloader(object):
    """
    Provide automated loading of MECO energy data from exports in gzip-compressed XML.
    """

    def __init__(self):
        """
        Constructor.
        """

        self.logger = MSGLogger(__name__)
        self.configer = MSGConfiger()
        self.fileUtil = MSGFileUtil()


    def newDataExists(self):
        """
        Check the data autoload folder for the presence of new data.

        :returns: True if new data exists.
        """

        autoloadPath = self.configer.configOptionValue('MECO Autoload', 'meco_new_data_path')
        if not self.fileUtil.validDirectory(autoloadPath):
            raise Exception('InvalidDirectory', '%s' % autoloadPath)

        patterns = ['*.gz']
        matchCnt = 0
        for root, dirs, filenames in os.walk(autoloadPath):
            for pat in patterns:
                for filename in fnmatch.filter(filenames, pat):
                    print filename
                    matchCnt += 1
        if matchCnt > 0:
            return True
        else:
            return False


    def loadNewData(self):
        """
        Load new data contained in the new data path.
        """

        autoloadPath = self.configer.configOptionValue('MECO Autoload', 'meco_new_data_path')
        command = self.configer.configOptionValue('MECO Autoload', 'data_load_command')
        os.chdir(autoloadPath)

        try:
            subprocess.check_call(command, shell = True)
        except subprocess.CalledProcessError, e:
            self.logger.log("An exception occurred: %s" % e, 'error')


    def archiveLoadedData(self):
        """
        Archive successfully loaded data.
        """
        autoloadPath = self.configer.configOptionValue('MECO Autoload', 'meco_new_data_path')
        archivePath = self.configer.configOptionValue('MECO Autoload', 'meco_autoload_archive_path')
        patterns = ['*.gz']
        for root, dirs, filenames in os.walk(autoloadPath):
            for pat in patterns:
                for filename in fnmatch.filter(filenames, pat):
                    os.rename('%s/%s' % (autoloadPath, filename), '%s/%s' % (archivePath, filename))


if __name__ == '__main__':
    autoloader = MECODataAutoloader()
    print "Testing MECO Data Autoloading"
    print "New data exists is %s" % autoloader.newDataExists()
