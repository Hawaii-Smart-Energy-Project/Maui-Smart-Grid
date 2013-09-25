#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'
__copyright__ = 'Copyright (c) 2013, University of Hawaii Smart Energy Project'
__license__ = 'https://raw.github' \
              '.com/Hawaii-Smart-Energy-Project/Maui-Smart-Grid/master/BSD' \
              '-LICENSE.txt'

from msg_logger import MSGLogger
from msg_configer import MSGConfiger

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


    def newDataExists(self):
        """
        Check the data autoload folder for the presence of new data.
        """

        autoloadPath = self.configer.configOptionValue('MECO Autoload', 'meco_new_data_path')


    def validDirectory(self, path):
        """
        Verify that the path is a valid directory.
        """
        pass


    def loadNewData(self):
        """
        Load new data contained in the new data path.
        """
        pass


    def archiveLoadedData(self):
        """
        Archive successfully loaded data.
        """
        pass
