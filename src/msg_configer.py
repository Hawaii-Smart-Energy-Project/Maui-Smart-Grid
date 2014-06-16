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
from msg_logger import MSGLogger

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
        self.logger = MSGLogger(__name__, 'INFO')

        # Define tables that will have data inserted. Data will only be inserted
        # to tables that are defined here.
        self.insertTables = (
            'MeterData', 'RegisterData', 'RegisterRead', 'Tier', 'Register',
            'IntervalReadData', 'Interval', 'Reading', 'EventData', 'Event')

        # Check permissions on the config file. Refuse to run if the permissions
        # are not set appropriately.

        configFilePath = '~/.msg-data-operations.cfg'

        if self.isMoreThanOwnerReadableAndWritable(
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


    def isMoreThanOwnerReadableAndWritable(self, filePath):
        """
        Determines if a file has greater permissions than owner read/write.
        :param filePath: String for path to the file being tested.
        :returns: Boolean True if the permissions are greater than owner
        read/write, otherwise return False.
        """

        st = os.stat(filePath)

        # Permissions are too permissive if group or others can read,
        # write or execute.
        if bool(st.st_mode & stat.S_IRGRP) or bool(
                        st.st_mode & stat.S_IROTH) or bool(
                        st.st_mode & stat.S_IWGRP) or bool(
                        st.st_mode & stat.S_IWOTH) or bool(
                        st.st_mode & stat.S_IXGRP) or bool(
                        st.st_mode & stat.S_IXOTH):
            return True
        else:
            return False
