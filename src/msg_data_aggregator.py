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
from msg_notifier import MSGNotifier
from msg_configer import MSGConfiger


class MSGDataAggregator(object):
    """
    Use for continuous data aggregation of diverse data types relevant to the
    Maui Smart Grid project.

    This is being implemented externally for performance and flexibility
    advantages over alternative approaches such as creating a view. It may be
    rolled into an internal function at future time if that proves to be
    beneficial.
    """

    @property
    def rawIrradianceCols(self):
        self._rawIrradianceCols = self.dbUtil.columnsString(self.cursor,
                                                            self.tables[
                                                                'irradiance'])
        return self._rawIrradianceCols

    @property
    def aggregatedIrradianceCols(self):
        self._aggregatedIrradianceCols = self.dbUtil.columnsString(self.cursor,
                                                                   self.tables[
                                                                       'agg_irradiance'])
        return self._aggregatedIrradianceCols

    @property
    def rawWeatherCols(self):
        self._rawWeatherCols = self.dbUtil.columnsString(self.cursor,
                                                         self.tables['weather'])
        return self._rawWeatherCols

    @property
    def aggregatedWeatherCols(self):
        self._aggregatedWeatherCols = self.dbUtil.columnsString(self.cursor,
                                                                self.tables[
                                                                    'agg_weather'])
        return self._aggregatedWeatherCols

    @property
    def rawCircuitCols(self):
        self._rawCircuitCols = self.dbUtil.columnsString(self.cursor,
                                                         self.tables['circuit'])
        return self._rawCircuitCols

    @property
    def aggregatedCircuitCols(self):
        self._aggregatedCircuitCols = self.dbUtil.columnsString(self.cursor,
                                                                self.tables[
                                                                    'agg_circuit'])
        return self._aggregatedCircuitCols

    @property
    def rawEgaugeCols(self):
        self._rawEgaugeCols = self.dbUtil.columnsString(self.cursor,
                                                        self.tables['egauge'])
        return self._rawEgaugeCols

    @property
    def aggregatedEgaugeCols(self):
        self._aggregatedEgaugeCols = self.dbUtil.columnsString(self.cursor,
                                                               self.tables[
                                                                   'agg_egauge'])
        return self._aggregatedEgaugeCols

    def __init__(self):
        """
        Constructor.
        """

        self.logger = MSGLogger(__name__, 'DEBUG')
        self.configer = MSGConfiger()
        self.connector = MSGDBConnector()
        self.cursor = self.connector.conn.cursor()
        self.dbUtil = MSGDBUtil()
        self.__nextMinuteCrossing = 0
        section = 'Aggregation'
        tableList = ['irradiance', 'agg_irradiance', 'weather', 'agg_weather',
                     'circuit', 'agg_circuit', 'egauge', 'agg_egauge']
        self.tables = {}
        for t in tableList:
            self.tables[t] = self.configer.configOptionValue(section,
                                                             '%s_table' % t)

    def aggregateIrradianceData(self, startDate = '', endDate = ''):
        """
        Perform aggregation of irradiance data And insert or update,
        as necessary, the aggregated data table in the database.

        :param startDate
        :param endDate
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


    def __intervalCrossed(self, minute):
        """
        :returns: True if an interval was crossed, False otherwise.
        """

        if minute >= self.__nextMinuteCrossing and minute <= 60 and self\
                .__nextMinuteCrossing != 0:
            self.__nextMinuteCrossing += 15
            if self.__nextMinuteCrossing >= 60:
                self.__nextMinuteCrossing = 0
            return True
        elif self.__nextMinuteCrossing == 0 and minute >= 0 and minute <= 15:
            self.__nextMinuteCrossing = 15
            return True
        return False

    def __dataAverage(self, sum, cnt, timestamp):
        """
        Return the averaged data along with the timestamp.

        :param sum
        :param cnt
        :param timestamp: This is the timestamp that is emitted.
        :returns: None
        """

        myCount = 0
        idx = 0
        for item in sum:
            myCount += 1
            if cnt[idx] != 0:
                print '%s, %s, %s' % (myCount, timestamp, item / cnt[idx])
            else:
                print '%s, %s, %s' % (myCount, timestamp, 'NULL')
            idx += 1

    def __generateAggregatedIrradianceData(self):
        """
        :returns:
        """

        pass

    def fetchIrradianceData(self, startDate, endDate):
        """
        :returns:
        """

        sql = """SELECT (%s) FROM
        "%s" WHERE timestamp BETWEEN '%s' AND '%s' ORDER BY
        timestamp, sensor_id""" % (
            self.rawIrradianceCols, self.tables['irradiance'], startDate,
            endDate)
        self.logger.log('sql: %s' % sql)
        self.dbUtil.executeSQL(self.cursor, sql)
        rows = self.cursor.fetchall()
        return rows

    def fetchWeatherData(self, startDate, endDate):
        """
        :returns:
        """

        sql = """SELECT %s FROM
        "%s" WHERE timestamp BETWEEN '%s' AND '%s' ORDER BY timestamp""" % (
            self.rawWeatherCols, self.tables['weather'], startDate, endDate)
