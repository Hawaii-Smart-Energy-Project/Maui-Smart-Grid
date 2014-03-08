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
from msg_aggregated_data import MSGAggregatedData

MINUTE_POSITION = 4  # In time tuple.


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
        self.cursor = MSGDBConnector().connectDB().cursor()
        self.dbUtil = MSGDBUtil()
        self.notifier = MSGNotifier()
        self.mathUtil = MSGMathUtil()
        self.irradianceSensorCount = 4
        self.__nextMinuteCrossing = 0
        section = 'Aggregation'
        tableList = ['irradiance', 'agg_irradiance', 'weather', 'agg_weather',
                     'circuit', 'agg_circuit', 'egauge', 'agg_egauge']
        self.columns = {}
        self.tables = {
            t: self.configer.configOptionValue(section, '%s_table' % t) for t in
            tableList}

        for t in self.tables.keys():
            self.logger.log('t:%s' % t, 'DEBUG')
            try:
                self.columns[t] = self.dbUtil.columnsString(self.cursor,
                                                            self.tables[t])
            except TypeError as error:
                self.logger.log('Ignoring missing table.')

    def __intervalCrossed(self, minute = None):
        """
        Determine interval crossing. Intervals are at 0, 15, 45, 60 min.

        :param minute: The integer value of the minute.
        :returns: True if an interval was crossed, False otherwise.
        """

        if not minute and minute != 0:
            raise (Exception, 'Minute not defined.')

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


    def __fetch(self, sql):
        """

        :param sql: Command to be executed.
        :returns: DB result set.
        """

        self.logger.log('sql: %s' % sql, 'debug')
        self.dbUtil.executeSQL(self.cursor, sql)
        return self.cursor.fetchall()


    def __rawData(self, dataType = '', orderBy = None, timestampCol = '',
                  startDate = '', endDate = ''):
        """

        :param dataType: string
        :param orderBy: list
        :param timestampCol: string
        :param startDate: string
        :param endDate: string
        :return: DB rows.
        """

        # @todo Validate args.

        return self.__fetch("""SELECT %s FROM "%s" WHERE %s BETWEEN '%s' AND
        '%s' ORDER BY
            %s""" % (
            self.columns[dataType], self.tables[dataType], timestampCol,
            startDate, endDate, ','.join(orderBy)))

    def __writeAggregatedData(self, dataType = '', aggDataCols = None,
                              aggData = None):

        if not aggDataCols:
            raise (Exception, 'aggDataCols not defined.')
        if not aggData:
            raise (Exception, 'aggData not defined.')

        dataCols = ','.join(aggDataCols)
        for row in aggData:
            success = True
            self.logger.log(
                'sql: %s' % ("""INSERT INTO "%s" (%s) VALUES (%s)""" % (
                    self.tables[dataType], dataCols, row)))
            # success = self.dbUtil.executeSQL(
            # """INSERT INTO "%s" (%s) VALUES (%s)""" % (
            #     self.tables[dataType], dataCols, row))
            if not success:
                raise (Exception, 'Failure during aggregated data insert.')


    def __irradianceIntervalAverages(self, sum, cnt, timestamp):
        """
        Perform averaging of an irradiance data interval.
        Return one collection per sensor.

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


    def __weatherIntervalAverages(self, sum, cnt, timestamp, tempIndex,
                                  humIndex):
        """
        Return one collection per timestamp.

        :param sum:
        :param cnt:
        :param timestamp:
        :param tempIndex: temperature index
        :param humIndex: humidity index
        :returns:
        """

        myAvgs = []
        tAvg = 'NULL'
        hAvg = 'NULL'
        if cnt[tempIndex] != 0:
            tAvg = sum[tempIndex] / cnt[tempIndex]
        if cnt[humIndex] != 0:
            hAvg = sum[humIndex] / cnt[humIndex]
        myAvgs.append([timestamp, tAvg, hAvg])
        return myAvgs


    def __circuitIntervalAverages(self, sums, cnts, timestamp, timestampIndex):
        """

        :param sums: dict
        :param cnts: dict
        :param timestamp: datetime
        :param timestampIndex: int
        :return: dict with circuits as keys for lists of aggregated values.
        """

        myAvgs = {}

        for k in sums.keys():

            myAvgs[k] = []
            sumIndex = 0
            for s in sums[k]:
                if sumIndex == timestampIndex:
                    myAvgs[k].append(timestamp)
                else:
                    if cnts[k][sumIndex] != 0:
                        myAvgs[k].append(s / cnts[k][sumIndex])
                    else:
                        myAvgs[k].append('NULL')
                sumIndex += 1

        return myAvgs


    def __egaugeIntervalAverages(self, sums, cnts, timestamp, timestampIndex):
        """

        :param sums:
        :param cnts:
        :param timestamp:
        :param timestampIndex:
        :returns:
        """

        myAvgs = {}

        for k in sums.keys():
            myAvgs[k] = []
            sumIndex = 0
            for s in sums[k]:
                if sumIndex == timestampIndex:
                    myAvgs[k].append(timestamp)
                else:
                    if cnts[k][sumIndex] != 0:
                        myAvgs[k].append(s / cnts[k][sumIndex])
                    else:
                        myAvgs[k].append('NULL')
                sumIndex += 1
        return myAvgs


    def aggregatedEgaugeData(self, startDate, endDate):
        """

        :param startDate:
        :param endDate:
        :returns: MSGAggregatedData
        """

        myDataType = 'egauge'
        timeCol = 'datetime'
        idCol = 'egauge_id'
        aggData = []
        ci = lambda col_name: self.columns[myDataType].split(',').index(
            col_name)

        rowCnt = 0

        def __egaugeIDs():
            egauges = set()
            # @todo Optimize using a distinct query.
            for row in self.__rawData(dataType = myDataType,
                                      orderBy = [timeCol, idCol],
                                      timestampCol = timeCol,
                                      startDate = startDate, endDate = endDate):
                egauges.add(row[ci(idCol)])
            return egauges

        egauges = __egaugeIDs()

        def __initSumAndCount():
            sums = {}
            cnts = {}

            for i in range(len(self.columns[myDataType].split(','))):
                for e in egauges:
                    if e not in sums.keys():
                        sums[e] = []
                        cnts[e] = []
                    sums[e].append(0)
                    cnts[e].append(0)
            return (sums, cnts)

        (sum, cnt) = __initSumAndCount()
        for row in self.__rawData(dataType = myDataType,
                                  orderBy = [timeCol, idCol],
                                  timestampCol = timeCol, startDate = startDate,
                                  endDate = endDate):
            for col in self.columns[myDataType].split(','):
                if self.mathUtil.isNumber(row[ci(col)]):
                    sum[row[ci(idCol)]][ci(col)] += row[ci(col)]
                    cnt[row[ci(idCol)]][ci(col)] += 1

            if (self.__intervalCrossed(
                    minute = row[ci(timeCol)].timetuple()[MINUTE_POSITION])):
                aggData += [
                    self.__egaugeIntervalAverages(sum, cnt, row[ci(timeCol)],
                                                  ci(timeCol))]
                __initSumAndCount()
            rowCnt += 1

        return MSGAggregatedData(columns = self.columns[myDataType],
                                 data = aggData)


    def aggregatedCircuitData(self, startDate, endDate):
        """

        :param startDate: str
        :param endDate: str
        :returns: MSGAggregatedData
        """

        myDataType = 'circuit'
        timeCol = 'timestamp'
        idCol = 'circuit'
        aggData = []
        ci = lambda col_name: self.columns['circuit'].split(',').index(col_name)
        assert (
            map(ci, ['timestamp', 'circuit', 'amp_a', 'amp_b', 'amp_c', 'mvar',
                     'mw']) is not None)

        rowCnt = 0

        def __circuits():
            circuits = set()
            # @todo Optimize using a distinct query.
            for row in self.__rawData(dataType = myDataType,
                                      orderBy = [timeCol, idCol],
                                      timestampCol = timeCol,
                                      startDate = startDate, endDate = endDate):
                circuits.add(row[ci(idCol)])
            return circuits

        circuits = __circuits()
        self.logger.log('circuits %s' % circuits)

        def __initSumAndCount():
            """
            Initialize storage dicts.
            """
            sum = {}
            cnt = {}

            for i in range(len(self.columns[myDataType].split(','))):
                for c in circuits:
                    if c not in sum.keys():
                        sum[c] = []
                        cnt[c] = []
                    sum[c].append(0)
                    cnt[c].append(0)
            return (sum, cnt)

        (sum, cnt) = __initSumAndCount()

        for row in self.__rawData(dataType = myDataType,
                                  orderBy = [timeCol, idCol],
                                  timestampCol = timeCol, startDate = startDate,
                                  endDate = endDate):
            for col in self.columns[myDataType].split(','):
                if self.mathUtil.isNumber(row[ci(col)]):
                    sum[row[ci(idCol)]][ci(col)] += row[ci(col)]
                    cnt[row[ci(idCol)]][ci(col)] += 1

            if (self.__intervalCrossed(
                    minute = row[ci(timeCol)].timetuple()[MINUTE_POSITION])):
                aggData += [
                    self.__circuitIntervalAverages(sum, cnt, row[ci(timeCol)],
                                                   ci(timeCol))]

                __initSumAndCount()
            rowCnt += 1

        return MSGAggregatedData(columns = self.columns[myDataType],
                                 data = aggData)


    def aggregatedWeatherData(self, startDate, endDate):
        """

        :param startDate: str
        :param endDate: str
        :returns: MSGAggregatedData
        """

        myDataType = 'weather'
        timeCol = 'timestamp'
        aggData = []
        ci = lambda col_name: self.columns[myDataType].split(',').index(
            col_name)
        assert (
            map(ci, ['timestamp', 'met_air_temp_degf',
                     'met_rel_humid_pct']) is not None)

        rowCnt = 0

        def __initSumAndCount():
            """
            Initialize storage arrays.
            """
            sum = []
            cnt = []

            # An extra column is created for generalization convenience.
            for i in range(len(self.columns[myDataType].split(','))):
                sum.append(0)
                cnt.append(0)
            return (sum, cnt)

        (sum, cnt) = __initSumAndCount()

        for row in self.__rawData(dataType = myDataType, orderBy = [timeCol],
                                  timestampCol = timeCol, startDate = startDate,
                                  endDate = endDate):
            for col in self.columns[myDataType].split(','):
                if self.mathUtil.isNumber(row[ci(col)]):
                    sum[ci(col)] += row[ci(col)]
                    cnt[ci(col)] += 1

            if (self.__intervalCrossed(
                    minute = row[ci(timeCol)].timetuple()[MINUTE_POSITION])):
                aggData += self.__weatherIntervalAverages(sum, cnt,
                                                          row[ci(timeCol)], ci(
                        'met_air_temp_degf'), ci('met_rel_humid_pct'))
                __initSumAndCount()
            rowCnt += 1

        return MSGAggregatedData(columns = self.columns[myDataType],
                                 data = aggData)


    def aggregatedIrradianceData(self, startDate, endDate):
        """
        Perform aggregation of irradiance data And insert or update,
        as necessary, the aggregated data table in the database.

        :param startDate: str
        :param endDate: str
        :returns: MSGAggregatedData
        """

        myDataType = 'irradiance'
        idCol = 'sensor_id'
        timeCol = 'timestamp'
        aggData = []
        ci = lambda col_name: self.columns[myDataType].split(',').index(
            col_name)
        assert (
            map(ci,
                ['sensor_id', 'timestamp', 'irradiance_w_per_m2']) is not None)

        sensorCount = self.irradianceSensorCount

        def __initSumAndCount():
            """
            Initialize storage arrays.
            """
            sum = []
            cnt = []
            for i in range(sensorCount):
                sum.append([])
                sum[i] = 0
                cnt.append([])
                cnt[i] = 0
            return (sum, cnt)

        (sum, cnt) = __initSumAndCount()

        rowCnt = 0

        for row in self.__rawData(dataType = myDataType,
                                  orderBy = [timeCol, idCol],
                                  timestampCol = timeCol, startDate = startDate,
                                  endDate = endDate):
            # cnt is used for sensor ID here.
            if self.mathUtil.isNumber(row[ci('irradiance_w_per_m2')]):
                # Add up the values for each sensor.
                cnt[row[ci(idCol)] - 1] += 1
                sum[row[ci(idCol)] - 1] += row[ci('irradiance_w_per_m2')]

            if (self.__intervalCrossed(
                    minute = row[ci(timeCol)].timetuple()[MINUTE_POSITION])):
                # Emit the average for the current sum.
                # Use the current timestamp that is the trailing timestamp
                # for the interval.
                aggData += self.__irradianceIntervalAverages(sum, cnt,
                                                             row[ci(timeCol)])
                __initSumAndCount()

            rowCnt += 1

            # @REVIEWED
            # Useful for debugging:
            # if rowCnt > 40000:
            #     return aggData
        return MSGAggregatedData(columns = self.columns[myDataType],
                                 data = aggData)



