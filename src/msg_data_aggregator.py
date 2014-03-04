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

    Four data types are supported:

    1. Irradiance
    2. Temperature/Humidity
    3. Circuit
    4. eGauge

    Aggregation is performed in-memory and saved to the DB.

    This is being implemented externally for performance and flexibility
    advantages over alternative approaches such as creating a view. It may be
    rolled into an internal function at future time if that proves to be
    beneficial.

    Usage:

        from msg_data_aggregator import MSGDataAggregator
        aggregator = MSGDataAggregator()

    """

    def __init__(self):
        """
        Constructor.
        """

        self.logger = MSGLogger(__name__, 'DEBUG')
        self.configer = MSGConfiger()
        try:
            self.cursor = MSGDBConnector().connectDB().cursor()
        except AttributeError as error:
            self.logger.log('Error while getting cursor: %s' % error, 'ERROR')
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

    def __intervalCrossed(self, minute):
        """
        Determine interval crossing. Intervals are at 0, 15, 45, 60 min.

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
        :returns: Averaged data tuple.
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

    def __rawIrradianceData(self, startDate, endDate):
        """
        :returns: Raw irradiance data as DB rows.
        """

        dataType = 'irradiance'
        return self.__fetch("""SELECT %s FROM "%s" WHERE timestamp BETWEEN
        '%s' AND '%s'
            ORDER BY timestamp, sensor_id""" % (
            self.columns[dataType], self.tables[dataType], startDate, endDate))

    def __rawWeatherData(self, startDate, endDate):
        """
        :returns: Raw weather data as DB rows.
        """

        dataType = 'weather'
        return self.__fetch("""SELECT %s FROM "%s" WHERE timestamp BETWEEN
        '%s' AND '%s'
            ORDER BY timestamp""" % (
            self.columns[dataType], self.tables[dataType], startDate, endDate))

    def __rawCircuitData(self, startDate, endDate):
        """
        :returns: Raw circuit data as DB rows.
        """

        dataType = 'circuit'
        return self.__fetch("""SELECT %s FROM "%s" WHERE timestamp BETWEEN
        '%s' AND '%s'
            ORDER BY timestamp""" % (
            self.columns[dataType], self.tables[dataType], startDate, endDate))

    def __rawEgaugeData(self, startDate, endDate):
        """
        :returns: Raw eGauge data as DB rows.
        """

        dataType = 'egauge'
        return self.__fetch("""SELECT %s FROM "%s" WHERE datetime BETWEEN
        '%s' AND '%s'
            ORDER BY datetime""" % (
            self.columns[dataType], self.tables[dataType], startDate, endDate))


    def __getNextMinuteCrossing(self, minute):
        if minute < 15:
            return 15
        elif minute < 30:
            return 30
        elif minute < 45:
            return 45
        else:
            return 0

    def aggregatedWeatherData(self, startDate, endDate):
        """

        :param startDate:
        :param endDate:
        :returns: List of tuples for aggregated data.
        """

        aggData = []
        ci = lambda col_name: self.columns['weather'].split(',').index(col_name)
        assert (
            map(ci, ['timestamp', 'met_air_temp_degf',
                     'met_rel_humid_pct']) is not None)

        rowCnt = 0
        sum = []
        cnt = []

        for col in ['met_air_temp_degf', 'met_rel_humid_pct']:
            sum[ci(col)].append(0)
            cnt[ci(col)].append(0)

        for row in self.__rawWeatherData(startDate, endDate):
            for col in ['met_air_temp_degf', 'met_rel_humid_pct']:
                if self.mathUtil.isNumber(row[ci(col)]):
                    sum[ci(col)] += row[ci(col)]
                    cnt[ci(col)] += 1

            minute = row[0].timetuple()[4]

        return aggData


    def aggregatedIrradianceData(self, startDate, endDate):
        """
        Perform aggregation of irradiance data And insert or update,
        as necessary, the aggregated data table in the database.

        :param startDate
        :param endDate
        :returns: List of tuples for aggregated data.
        """

        aggData = []
        ci = lambda col_name: self.columns['irradiance'].split(',').index(
            col_name)
        assert (
            map(ci,
                ['sensor_id', 'timestamp', 'irradiance_w_per_m2']) is not None)

        sensorCount = 4

        sum = []
        cnt = []

        for i in range(sensorCount):
            sum.append([])
            sum[i] = 0
            cnt.append([])
            cnt[i] = 0

        rowCnt = 0

        for row in self.__rawIrradianceData(startDate, endDate):

            if self.mathUtil.isNumber(row[ci('irradiance_w_per_m2')]):
                # Add up the values for each sensor.
                cnt[row[ci('sensor_id')] - 1] += 1
                sum[row[ci('sensor_id')] - 1] += row[ci('irradiance_w_per_m2')]

            minute = row[ci('timestamp')].timetuple()[4]

            if (self.__intervalCrossed(minute)):
                # Emit the average for the current sum.
                # Use the current timestamp that is the trailing timestamp
                # for the interval.
                aggData += self.__irradianceIntervalAverages(sum, cnt, row[
                    ci('timestamp')])

                sum = []
                cnt = []
                for i in range(sensorCount):
                    sum.append([])
                    sum[i] = 0
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
