#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'
__copyright__ = 'Copyright (c) 2014, University of Hawaii Smart Energy Project'
__license__ = 'https://raw.github' \
              '.com/Hawaii-Smart-Energy-Project/Maui-Smart-Grid/master/BSD' \
              '-LICENSE.txt'

from msg_logger import MSGLogger
from msg_db_connector import MSGDBConnector
from msg_db_util import MSGDBUtil


class MSGDataAggregator(object):
    """
    Use for continuous data aggregation of diverse data types relevant to the
    Maui Smart Grid project.
    """

    @property
    def rawIrradianceCols(self):
        self._rawIrradianceCols = self.dbUtil.columns(self.cursor,
                                                      'IrradianceData')
        return self._rawIrradianceCols

    @property
    def aggregatedIrradianceCols(self):
        self._aggregatedIrradianceCols = self.dbUtil.columns(self.cursor,
                                                             'AverageFifteenMinIrradianceData')
        return self._aggregatedIrradianceCols

    @property
    def aggregatedWeatherCols(self):
        self._aggregatedWeatherCols = self.dbUtil.columns(self.cursor,
                                                          'AverageFifteenMinKiheiSCADATemperatureHumidity')
        return self._aggregatedWeatherCols

    @property
    def aggregatedCircuitCols(self):
        self._aggregatedCircuitCols = None
        return self._aggregatedCircuitCols

    @property
    def aaggregatedEgaugeCols(self):
        self._aggregatedEgaugeCols = None
        return self._aggregatedEgaugeCols

    def __init__(self):
        """
        Constructor.
        """
        self.logger = MSGLogger(__name__, 'DEBUG')
        self.cursor = MSGDBConnector().conn.cursor()
        self.dbUtil = MSGDBUtil()

    def aggregateIrradianceData(self):
        """
        Perform aggregation of irradiance data And insert or update,
        as necessary, the aggregated data table in the database.

        :returns:
        """

        pass

    def aggregateWeatherData(self):
        """
        :returns:
        """
        pass

    def aggregateCircuitData(self):
        """
        :returns:
        """
        pass

    def aggregateEgaugeData(self):
        """
        :returns:
        """
        pass

