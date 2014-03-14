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
from datetime import datetime
import copy

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

    The general data form conforms to

    1. timestamp, subkey_id, val1, val2, val3, ...
    2. timestamp, val1, val2, val3, ...

    Case (2) is handled within the same space as (1) by testing for the
    existence of subkeys.

    Aggregation is performed in-memory and saved to the DB. The time range is
    delimited by start date and end date where the values are included in the
    range.

    Aggregation subkeys are values such as eGauge IDs or circuit numbers.

    @todo Generalize to a single aggregation provider and single averaging
    method.

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

        self.logger = MSGLogger(__name__, 'INFO')
        self.configer = MSGConfiger()
        self.conn = MSGDBConnector().connectDB()
        self.cursor = self.conn.cursor()
        self.dbUtil = MSGDBUtil()
        self.notifier = MSGNotifier()
        self.mathUtil = MSGMathUtil()
        self.irradianceSensorCount = 4
        self.nextMinuteCrossing = {}
        self.nextMinuteCrossingWithoutSubkeys = None
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


    def intervalCrossed(self, minute = None, subkey = None):
        """
        Determine interval crossing. Intervals are at 0, 15, 45, 60 min.

        :param minute: The integer value of the minute.
        :param subkey: The name for the subkey used for aggregation.
        :returns: True if an interval was crossed, False otherwise.
        """

        if not minute and minute != 0:
            raise Exception('Minute not defined.')

        intervalSize = 15
        first = 0
        last = 60

        if subkey is not None:
            if minute >= self.nextMinuteCrossing[subkey] and minute <= last \
                    and \
                            self.nextMinuteCrossing[subkey] != first:
                self.nextMinuteCrossing[subkey] += intervalSize
                if self.nextMinuteCrossing[subkey] >= last:
                    self.nextMinuteCrossing[subkey] = first
                self.logger.log('minute crossed at #1.', 'debug')
                return True
            elif self.nextMinuteCrossing[
                subkey] == first and minute >= first and minute <= intervalSize:
                self.nextMinuteCrossing[subkey] = intervalSize
                self.logger.log('minute crossed at #2.', 'debug')
                return True
            return False
        else:
            if minute >= self.nextMinuteCrossingWithoutSubkeys and minute <= \
                    last and self.nextMinuteCrossingWithoutSubkeys != first:
                self.nextMinuteCrossingWithoutSubkeys += intervalSize
                if self.nextMinuteCrossingWithoutSubkeys >= last:
                    self.nextMinuteCrossingWithoutSubkeys = first
                self.logger.log('minute crossed at #3.', 'debug')
                return True
            elif self.nextMinuteCrossingWithoutSubkeys == first and minute >=\
                    first and minute <= intervalSize:
                self.nextMinuteCrossingWithoutSubkeys = intervalSize
                self.logger.log('minute crossed at #4.', 'debug')
                return True
            return False


    def rows(self, sql):
        """

        :param sql: Command to be executed.
        :returns: DB result set.
        """

        self.logger.log('sql: %s' % sql, 'debug')
        self.dbUtil.executeSQL(self.cursor, sql)
        return self.cursor.fetchall()


    def rawData(self, dataType = '', orderBy = None, timestampCol = '',
                startDate = '', endDate = ''):
        """

        :param dataType: string
        :param orderBy: list
        :param timestampCol: string
        :param startDate: string
        :param endDate: string
        :returns: DB rows.
        """

        # @todo Validate args.

        orderBy = filter(None, orderBy)

        return self.rows("""SELECT %s FROM "%s" WHERE %s BETWEEN '%s' AND
        '%s' ORDER BY
            %s""" % (
            self.columns[dataType], self.tables[dataType], timestampCol,
            startDate, endDate, ','.join(orderBy)))


    def subkeys(self, dataType = '', timestampCol = '', subkeyCol = '',
                startDate = '', endDate = ''):
        """

        :param dataType:
        :param timestampCol:
        :param subkeyCol:
        :param startDate:
        :param endDate:
        :returns:
        """

        return [sk[0] for sk in self.rows("""SELECT DISTINCT(%s) FROM "%s"
        WHERE %s BETWEEN '%s' AND '%s'
            ORDER BY %s""" % (
            subkeyCol, self.tables[dataType], timestampCol, startDate, endDate,
            subkeyCol))]


    def insertAggregatedData(self, dataType = '', aggDataCols = None,
                             aggData = None):

        if not aggDataCols:
            raise Exception('aggDataCols not defined.')
        if not aggData:
            raise Exception('aggData not defined.')

        print 'aggdata: %s' % aggData

        # @HIGHLIGHTED For debugging.
        self.dbUtil.executeSQL(self.cursor,
                               """DELETE FROM \"%s\"""" % self.tables[dataType])

        for row in aggData:

            for key in row.keys():
                values = ''
                valCnt = 0
                for val in row[key]:
                    if val == 'NULL':
                        values += val
                    elif type(val) == type(''):
                        values += "'" + val.strip() + "'"
                    elif isinstance(val, datetime):
                        values += "'" + val.isoformat() + "'"
                    elif type(val) == type(0):
                        values += str(val)
                    elif type(val) == type(0.0):
                        values += str(val)
                    else:
                        values += val
                    if valCnt < len(aggDataCols) - 1:
                        values += ","
                    valCnt += 1

                success = True
                # self.logger.log('sql: %s' % (
                #     """INSERT INTO "%s" (%s) VALUES (%s)""" % (
                #         self.tables[dataType], ','.join(aggDataCols),
                # values)))

                success = self.dbUtil.executeSQL(self.cursor, """INSERT INTO
                "%s" (%s)
                                                 VALUES (%s)""" % (
                    self.tables[dataType], ','.join(aggDataCols), values))
                if not success:
                    raise Exception('Failure during aggregated data insert.')
        self.conn.commit()


    def reportAggregation(self, rowCnt = 0):
        self.logger.log('Aggregating %d rows of data.' % rowCnt, 'warning')


    def intervalAverages(self, sums, cnts, timestamp, timestampIndex,
                         subkeyIndex = None, subkey = None):
        """
        Aggregates all data for the current interval for the given subkey.

        :param sums: list
        :param cnts: list
        :param timestamp: datetime
        :param timestampIndex: int
        :param subkeyIndex: int
        :param subkey: string
        :returns: Averaged data as a dict with form {subkey:data}
        """

        if subkey is not None:
            myAvgs = {}
            reportedAgg = False
            myAvgs[subkey] = []
            sumIndex = 0

            self.logger.log('key: %s' % subkey, 'critical')
            # Iterate over sums.
            for s in sums[subkey]:
                if sumIndex == timestampIndex:
                    myAvgs[subkey].append(timestamp)
                elif sumIndex == subkeyIndex:
                    myAvgs[subkey].append(subkey)
                else:
                    if cnts[subkey][sumIndex] != 0:
                        if not reportedAgg:
                            self.logger.log(
                                'Aggregating %d rows of data.' % cnts[subkey][
                                    sumIndex], 'warning')
                            reportedAgg = True

                        myAvgs[subkey].append(s / cnts[subkey][sumIndex])
                    else:
                        myAvgs[subkey].append('NULL')
                sumIndex += 1
            return myAvgs
        else:
            myAvgs = []
            reportedAgg = False
            sumIndex = 0
            for s in sums:
                if sumIndex == timestampIndex:
                    myAvgs.append(timestamp)
                else:
                    if cnts[sumIndex] != 0:
                        if not reportedAgg:
                            self.logger.log(
                                'Aggregating %d rows of data.' % cnts[sumIndex],
                                'warning')
                            reportedAgg = True
                        myAvgs.append(s / cnts[sumIndex])
                    else:
                        myAvgs.append('NULL')
                sumIndex += 1
            return myAvgs


    def aggregatedData(self, dataType = '', aggregationType = '',
                       timeColumnName = '', subkeyColumnName = '',
                       startDate = '', endDate = ''):
        """
        ***********************************************************************
        Provide aggregated data.
        ***********************************************************************

        :param dataType: string
        :param aggregationType: string
        :param timeColumnName: string
        :param subkeyColumnName: string
        :param startDate: string
        :param endDate: string
        :returns: MSGAggregatedData
        """

        aggData = []
        ci = lambda col_name: self.columns[dataType].split(',').index(col_name)

        rowCnt = 0

        mySubkeys = []
        if subkeyColumnName:
            mySubkeys = self.subkeys(dataType = dataType,
                                     timestampCol = timeColumnName,
                                     subkeyCol = subkeyColumnName,
                                     startDate = startDate, endDate = endDate)

        self.logger.log('subkeys: %s' % mySubkeys, 'debug')

        def __initSumAndCount(subkey = None):
            """
            """

            sums = {}
            cnts = {}

            if not mySubkeys:
                sums = []
                cnts = []
                for i in range(len(self.columns[dataType].split(','))):
                    sums.append(0)
                    cnts.append(0)
            else:
                if not subkey:
                    for i in range(len(self.columns[dataType].split(','))):
                        for k in mySubkeys:
                            if k not in sums.keys():
                                sums[k] = []
                                cnts[k] = []
                            sums[k].append(0)
                            cnts[k].append(0)
                else:
                    self.logger.log('resetting subkey %s' % subkey, 'critical')
                    sums[subkey] = []
                    sums[subkey].append(0)
                    cnts[subkey] = []
                    cnts[subkey].append(0)

            return (sums, cnts)

        (sum, cnt) = __initSumAndCount()

        def __initIntervalCrossings():
            """
            """

            subkeysToCheck = copy.copy(mySubkeys)
            self.logger.log('subkeys to check: %s' % subkeysToCheck, 'debug')

            if mySubkeys:
                for row in self.rawData(dataType = dataType,
                                        orderBy = [timeColumnName,
                                                   subkeyColumnName],
                                        timestampCol = timeColumnName,
                                        startDate = startDate,
                                        endDate = endDate):

                    # @CRITICAL: Exit after every subkey has been visited.
                    if subkeysToCheck != []:
                        subkeysToCheck.remove(row[ci(subkeyColumnName)])
                        minute = row[ci(timeColumnName)].timetuple()[
                            MINUTE_POSITION]

                        if minute <= 15:
                            self.nextMinuteCrossing[
                                row[ci(subkeyColumnName)]] = 15
                        elif minute <= 30:
                            self.nextMinuteCrossing[
                                row[ci(subkeyColumnName)]] = 30
                        elif minute <= 45:
                            self.nextMinuteCrossing[
                                row[ci(subkeyColumnName)]] = 45
                        elif minute == 0 or minute <= 59:
                            self.nextMinuteCrossing[
                                row[ci(subkeyColumnName)]] = 0
                        else:
                            raise Exception(
                                'Unable to determine next minute crossing')
                        self.logger.log('next min crossing for %s = %s' % (
                            row[ci(subkeyColumnName)],
                            self.nextMinuteCrossing[row[ci(subkeyColumnName)]]),
                                        'debug')
                    else:
                        break

            else:
                rowCnt = 0
                # @todo Optimize by querying only the first row.
                for row in self.rawData(dataType = dataType,
                                        orderBy = [timeColumnName],
                                        timestampCol = timeColumnName,
                                        startDate = startDate,
                                        endDate = endDate):
                    minute = row[ci(timeColumnName)].timetuple()[
                        MINUTE_POSITION]
                    if minute <= 15:
                        self.nextMinuteCrossingWithoutSubkeys = 15
                    elif minute <= 30:
                        self.nextMinuteCrossingWithoutSubkeys = 30
                    elif minute <= 45:
                        self.nextMinuteCrossingWithoutSubkeys = 45
                    elif minute == 0 or minute <= 59:
                        self.nextMinuteCrossingWithoutSubkeys = 0
                    else:
                        raise Exception(
                            'Unable to determine next minute crossing')
                    self.logger.log('next min crossing = %s' % (
                        self.nextMinuteCrossingWithoutSubkeys), 'debug')
                    rowCnt += 1
                    if rowCnt > 0:
                        break


        __initIntervalCrossings()

        for row in self.rawData(dataType = dataType,
                                orderBy = [timeColumnName, subkeyColumnName],
                                timestampCol = timeColumnName,
                                startDate = startDate, endDate = endDate):
            self.logger.log('row: %d ----> %s' % (rowCnt, str(row)), 'debug')

            if mySubkeys:
                for col in self.columns[dataType].split(','):
                    if self.mathUtil.isNumber(row[ci(col)]):
                        sum[row[ci(subkeyColumnName)]][ci(col)] += row[ci(col)]
                        cnt[row[ci(subkeyColumnName)]][ci(col)] += 1

                minute = row[ci(timeColumnName)].timetuple()[MINUTE_POSITION]

                if self.intervalCrossed(minute = minute,
                                        subkey = row[ci(subkeyColumnName)]):
                    self.logger.log('==> row: %s' % str(row), 'critical')
                    minuteCrossed = minute

                    # Perform aggregation on all of the previous data including
                    # the current data for the current subkey.
                    self.logger.log('key: %s' % row[ci(subkeyColumnName)],
                                    'warning')
                    aggData += [
                        self.intervalAverages(sum, cnt, row[ci(timeColumnName)],
                                              ci(timeColumnName),
                                              ci(subkeyColumnName),
                                              row[ci(subkeyColumnName)])]
                    self.logger.log('minute crossed %d' % minuteCrossed,
                                    'DEBUG')

                    # Init current sum and cnt for subkey that has a completed
                    # interval.
                    __initSumAndCount(subkey = row[ci(subkeyColumnName)])
            else:
                for col in self.columns[dataType].split(','):
                    if self.mathUtil.isNumber(row[ci(col)]):
                        sum[ci(col)] += row[ci(col)]
                        cnt[ci(col)] += 1

                minute = row[ci(timeColumnName)].timetuple()[MINUTE_POSITION]

                if self.intervalCrossed(minute = minute):
                    self.logger.log('==> row: %s' % str(row), 'critical')
                    minuteCrossed = minute

                    aggData += [
                        self.intervalAverages(sum, cnt, row[ci(timeColumnName)],
                                              ci(timeColumnName))]

            rowCnt += 1

        self.logger.log('aggdata = %s' % aggData, 'debug')
        return MSGAggregatedData(aggregationType = aggregationType,
                                 columns = self.columns[dataType].split(','),
                                 data = aggData)



