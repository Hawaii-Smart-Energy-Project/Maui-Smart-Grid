#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'

import ConfigParser, os
import sys

class MECOConfiger(object) :
    """Supports system-specific configuration for MECO data processing.
    The site configuration file is located in ~/.meco-data-operations.cfg.
    """

    def __init__(self) :
        """Constructor
        """

        self._config = ConfigParser.ConfigParser()

        # Define tables that will have data inserted.
        self.insertTables = (
            'MeterData', 'RegisterData', 'RegisterRead', 'Tier', 'Register', 'IntervalReadData',
            'Interval', 'Reading')

        try :
            self._config.read(['site.cfg', os.path.expanduser('~/.meco-data-operations.cfg')])
        except :
            print "Critical error: Failed to read site _config"
            sys.exit()


    def configOptionValue(self, section, option) :
        """Get a configuration value from the local configuration file.
        :param section
        :param option
        """

        try :
            return self._config.get(section, option)
        except :
            print "Failed when getting _config option %s in section %s" % (option, section)
            sys.exit()
