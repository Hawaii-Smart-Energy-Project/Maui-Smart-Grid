#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'


from mecodbconnect import MECODBConnector
from msg_config import MSGConfiger
from msg_logger import MSGLogger
import gzip


class MSGWeatherDataLoader(object):
    """
    Load NOAA weather data relevant to the MSG project.

    Hourly observations are loaded for the Kahului Airport weather station.
    """

    def __init__(self):
        """
        Constructor.
        """

        self.logger = MSGLogger(__name__, 'info')
        self.kahuluiStationID = '22516'
        self.stationIDs = [self.kahuluiStationID]

    def insertHourlyData(self):
        """
        Given an hourly data source, insert the relevant data to the data store.
        """

        pass
