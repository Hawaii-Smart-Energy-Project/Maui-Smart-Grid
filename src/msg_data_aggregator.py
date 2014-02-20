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
        self.columns = {}
        for t in tableList:
            self.tables[t] = self.configer.configOptionValue(section,
                                                             '%s_table' % t)
        for t in self.tables.keys():
            self.logger.log('t:%s' % t, 'DEBUG')
            try:
                self.columns[t] = self.dbUtil.columnsString(self.cursor,
                                                            self.tables[t])
            except TypeError as error:
                self.logger.log('Ignoring missing table.')


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
        Determine interval crossing.

        :param minute: The integer value of the minute.
        :returns: True if an interval was crossed, False otherwise.
        """

        intervalSize = 15
        first = 0
        last = 60
        if minute >= self.__nextMinuteCrossing and minute <= last and self\
                .__nextMinuteCrossing != first:
            self.__nextMinuteCrossing += intervalSize
            if self.__nextMinuteCrossing >= last:
                self.__nextMinuteCrossing = first
            return True
        elif self.__nextMinuteCrossing == first and minute >= first and \
                        minute <= intervalSize:
            self.__nextMinuteCrossing = intervalSize
            return True
        return False

    def averageIrradianceInterval(self, sum, cnt, timestamp):
        """
        Perform averaging of an irradiance data interval.

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

        dataType = 'irradiance'
        sql = """SELECT (%s) FROM
        "%s" WHERE timestamp BETWEEN '%s' AND '%s' ORDER BY
        timestamp, sensor_id""" % (
            self.columns[dataType], self.tables[dataType], startDate, endDate)
        return self.__fetch(sql)

    def fetchWeatherData(self, startDate, endDate):
        """
        :returns:
        """

        dataType = 'weather'
        sql = """SELECT %s FROM
        "%s" WHERE timestamp BETWEEN '%s' AND '%s' ORDER BY timestamp""" % (
            self.columns[dataType], self.tables[dataType], startDate, endDate)
        return self.__fetch(sql)

    def fetchCircuitData(self, startDate, endDate):
        """
        :returns:
        """

        dataType = 'circuit'
        sql = """SELECT (%s) FROM
        "%s" WHERE timestamp BETWEEN '%s' AND '%s' ORDER BY
        timestamp""" % (
            self.columns[dataType], self.tables[dataType], startDate, endDate)
        return self.__fetch(sql)

    def fetchEgaugeData(self, startDate, endDate):
        """
        :returns:
        """

        dataType = 'egauge'
        sql = """SELECT (%s) FROM
        "%s" WHERE datetime BETWEEN '%s' AND '%s' ORDER BY
        datetime""" % (
            self.columns[dataType], self.tables[dataType], startDate, endDate)
        return self.__fetch(sql)


    def __fetch(self, sql):
        """

        :param sql: Command to be executed.
        :returns: DB result set.
        """

        self.logger.log('sql: %s' % sql)
        self.dbUtil.executeSQL(self.cursor, sql)
        rows = self.cursor.fetchall()
        return rows
