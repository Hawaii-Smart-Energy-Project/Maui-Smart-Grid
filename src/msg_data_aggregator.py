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
from msg_math_util import MSGMathUtil


class MSGDataAggregator(object):
    """
    Use for continuous data aggregation of diverse data types relevant to the
    Maui Smart Grid project.

    Aggregation is performed in-memory and saved to the DB.

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
        # self.connector =
        self.cursor = MSGDBConnector().connectDB().cursor()
        self.dbUtil = MSGDBUtil()
        self.notifier = MSGNotifier()
        self.mathUtil = MSGMathUtil()
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

    def __irradianceIntervalAverages(self, sum, cnt, timestamp):
        """
        Perform averaging of an irradiance data interval.

        :param sum[]: Totals of values.
        :param cnt[]: Numbers of records
        :param timestamp: This is the timestamp that is emitted.
        :returns: averaged data tuple
        """

        myAvgs = []
        myCount = 0
        idx = 0
        for item in sum:
            myCount += 1
            if cnt[idx] != 0:
                myAvgs.append((myCount, timestamp, item / cnt[idx]))
            else:
                myAvgs.append((myCount, timestamp, 'NULL'))
            idx += 1
        return myAvgs

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
        return self.__fetch("""SELECT %s FROM "%s" WHERE timestamp BETWEEN
        '%s' AND '%s'
            ORDER BY timestamp, sensor_id""" % (
            self.columns[dataType], self.tables[dataType], startDate, endDate))

    def fetchWeatherData(self, startDate, endDate):
        """
        :returns:
        """

        dataType = 'weather'
        return self.__fetch("""SELECT %s FROM "%s" WHERE timestamp BETWEEN
        '%s' AND '%s'
            ORDER BY timestamp""" % (
            self.columns[dataType], self.tables[dataType], startDate, endDate))

    def fetchCircuitData(self, startDate, endDate):
        """
        :returns:
        """

        dataType = 'circuit'
        return self.__fetch("""SELECT %s FROM "%s" WHERE timestamp BETWEEN
        '%s' AND '%s'
            ORDER BY timestamp""" % (
            self.columns[dataType], self.tables[dataType], startDate, endDate))

    def fetchEgaugeData(self, startDate, endDate):
        """
        :returns:
        """

        dataType = 'egauge'
        return self.__fetch("""SELECT %s FROM "%s" WHERE datetime BETWEEN
        '%s' AND '%s'
            ORDER BY datetime""" % (
            self.columns[dataType], self.tables[dataType], startDate, endDate))


    def aggregatedIrradianceData(self, startDate, endDate):
        """
        Perform aggregation of irradiance data And insert or update,
        as necessary, the aggregated data table in the database.

        :param startDate
        :param endDate
        :returns: aggregated data
        """

        aggData = []
        ci = lambda col_name: self.columns['irradiance'].split(',').index(
            col_name)
        assert (
            map(ci,
                ['sensor_id', 'timestamp', 'irradiance_w_per_m2']) is not None)

        sensorCount = 4

        sum = []

        for i in range(sensorCount):
            sum.append([])
            sum[i] = 0

        cnt = []

        for i in range(sensorCount):
            cnt.append([])
            cnt[i] = 0

        rowCnt = 0

        for row in self.fetchIrradianceData(startDate, endDate):

            if self.mathUtil.isNumber(row[ci('irradiance_w_per_m2')]):
                # Add up the values for each sensor.
                cnt[row[ci('sensor_id')] - 1] += 1
                sum[row[ci('sensor_id')] - 1] += row[ci('irradiance_w_per_m2')]

            minute = row[ci('timestamp')].timetuple()[4]

            if rowCnt == 0:
                if minute < 15:
                    NEXT_MINUTE_CROSSING = 15
                elif minute < 30:
                    NEXT_MINUTE_CROSSING = 30
                elif minute < 45:
                    NEXT_MINUTE_CROSSING = 45
                else:
                    NEXT_MINUTE_CROSSING = 0

            if (self.__intervalCrossed(minute)):
                # Emit the average for the current sum.
                # Use the current timestamp that is the trailing timestamp
                # for the interval.
                aggData += self.__irradianceIntervalAverages(sum, cnt, row[
                    ci('timestamp')])

                sum = []
                for i in range(sensorCount):
                    sum.append([])
                    sum[i] = 0
                cnt = []
                for i in range(sensorCount):
                    cnt.append([])
                    cnt[i] = 0

            rowCnt += 1

            # @REVIEWED
            # Useful for debugging:
            # if rowCnt > 40000:
            #     return aggData
        return aggData

    def __fetch(self, sql):
        """

        :param sql: Command to be executed.
        :returns: DB result set.
        """

        self.logger.log('sql: %s' % sql)
        self.dbUtil.executeSQL(self.cursor, sql)
        return self.cursor.fetchall()
