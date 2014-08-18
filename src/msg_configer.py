#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'
__copyright__ = 'Copyright (c) 2014, University of Hawaii Smart Energy Project'
__license__ = 'https://raw.github' \
              '.com/Hawaii-Smart-Energy-Project/Maui-Smart-Grid/master/BSD' \
              '-LICENSE.txt'

import ConfigParser
import os
import stat
import sys
from sek.logger import SEKLogger
from sek.file_util import SEKFileUtil

class MSGConfiger(object):
    """
    Supports system-specific configuration for MECO data processing.
    The site-level configuration file is located in ~/.meco-data-operations.cfg.

    Usage:

    configer = MSGConfiger()

    """

    def __init__(self):
        """
        Constructor.
        """

        self._config = ConfigParser.ConfigParser()
        self.logger = SEKLogger(__name__, 'INFO')
        self.fileUtil = SEKFileUtil()

        # Define tables that will have data inserted. Data will only be inserted
        # to tables that are defined here.
        self.insertTables = (
            'MeterData', 'RegisterData', 'RegisterRead', 'Tier', 'Register',
            'IntervalReadData', 'Interval', 'Reading', 'EventData', 'Event')

        # Check permissions on the config file. Refuse to run if the permissions
        # are not set appropriately.

        configFilePath = '~/.msg-data-operations.cfg'

        if self.fileUtil.isMoreThanOwnerReadableAndWritable(
                os.path.expanduser(configFilePath)):
            self.logger.log(
                "Configuration file permissions are too permissive. Operation "
                "will not continue.", 'error')
            sys.exit()

        try:
            self._config.read(['site.cfg', os.path.expanduser(configFilePath)])
        except:
            self.logger.log("Critical error: The data in {} cannot be "
                            "accessed successfully.".format(configFilePath),
                            'ERROR')
            sys.exit(-1)


    def configOptionValue(self, section, option):
        """
        Get a configuration value from the local configuration file.
        :param section: String of section in config file.
        :param option: String of option in config file.
        :returns: The value contained in the configuration file.
        """

        try:
            configValue = self._config.get(section, option)
            if configValue == "True":
                return True
            elif configValue == "False":
                return False
            else:
                return configValue
        except:
            self.logger.log(
                "Failed when getting configuration option {} in section {"
                "}.".format(option, section), 'error')
            sys.exit(-1)


