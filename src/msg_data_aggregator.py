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
from msg_time_util import MSGTimeUtil
from itertools import groupby
from dateutil.relativedelta import relativedelta

MINUTE_POSITION = 4  # In a time tuple.
INTERVAL_DURATION = 15


class MSGDataAggregator(object):
    """
    Use for continuous data aggregation of diverse data types relevant to the
    Maui Smart Grid project.

    Four data types are supported:

    1. Irradiance
    2. Temperature/Humidity (weather)
    3. Circuit
    4. eGauge

    The general data form conforms to

    1. timestamp, subkey_id, val1, val2, val3, ...
    2. timestamp, val1, val2, val3, ...

    Case (2) is handled within the same space as (1) by testing for the
    existence of subkeys.

    Current aggregation consists of averaging over **15-min intervals**.

    Aggregation is performed in-memory and saved to the DB. The time range is
    delimited by start date and end date where the values are included in the
    range. The timestamps for aggregation intervals are the last timestamp in a
    respective series.

    * Aggregation subkeys are values such as eGauge IDs or circuit numbers.

    Aggregation is being implemented externally for performance and flexibility
    advantages over alternative approaches such as creating a view. It may be
    rolled into an internal function at future time if that proves to be
    beneficial.

    Usage:

        from msg_data_aggregator import MSGDataAggregator
        aggregator = MSGDataAggregator()

    API:

        aggregateAllData(dataType = dataType)

        aggregateNewData(dataType = dataType)

    """

    def __init__(self, exitOnError = True, commitOnEveryInsert = False,
                 testing = False):
        """
        Constructor.

        :param testing: if True, the testing DB will be connected instead of
        the production DB.
        """

        self.logger = MSGLogger(__name__, 'info')
        self.configer = MSGConfiger()
        self.conn = MSGDBConnector().connectDB()
        self.cursor = self.conn.cursor()
        self.dbUtil = MSGDBUtil()
        self.notifier = MSGNotifier()
        self.mathUtil = MSGMathUtil()
        self.timeUtil = MSGTimeUtil()
        self.nextMinuteCrossing = {}
        self.nextMinuteCrossingWithoutSubkeys = None
        self.exitOnError = exitOnError
        self.commitOnEveryInsert = commitOnEveryInsert
        section = 'Aggregation'
        tableList = ['irradiance', 'agg_irradiance', 'weather', 'agg_weather',
                     'circuit', 'agg_circuit', 'egauge', 'agg_egauge']
        self.dataParams = {'weather': ('agg_weather', 'timestamp', ''),
                           'egauge': ('agg_egauge', 'datetime', 'egauge_id'),
                           'circuit': ('agg_circuit', 'timestamp', 'circuit'),
                           'irradiance': (
                               'agg_irradiance', 'timestamp', 'sensor_id')}
        self.columns = {}

        # tables[datatype] gives the table name for datatype.
        self.tables = {
            t: self.configer.configOptionValue(section, '{}_table'.format(t))
            for t in tableList}

        for t in self.tables.keys():
            self.logger.log('t:{}'.format(t), 'DEBUG')
            try:
                self.columns[t] = self.dbUtil.columnsString(self.cursor,
                                                            self.tables[t])
            except TypeError as error:
                self.logger.log(
                    'Ignoring missing table: Error is {}.'.format(error),
                    'error')

    def existingIntervals(self, aggDataType = '', timeColumnName = ''):
        """
        Retrieve the existing aggregation intervals for the given data type.

        :param aggDataType: string
        :param timeColumnName: string
        :return: List of intervals.
        """

        return [x[0] for x in self.rows(
            """SELECT {0} from \"{1}\" ORDER BY {2}""".format(timeColumnName,
                                                              self.tables[
                                                                  aggDataType],
                                                              timeColumnName))]

    def unaggregatedIntervalCount(self, dataType = '', aggDataType = '',
                                  timeColumnName = '', idColumnName = ''):
        """
        Return count of unaggregated intervals for a given data type.
        :param dataType:
        :param aggDataType:
        :param timeColumnName:
        :param idColumnName:
        :return: int
        """

        return len(
            self.unaggregatedEndpoints(dataType, aggDataType, timeColumnName,
                                       idColumnName))


    def lastAggregationEndpoint(self, aggDataType = '', timeColumnName = ''):
        """
        Last aggregation endpoint for a given datatype.

        :param dataType:
        :param timeColumnName:
        :return:
        """

        return self.existingIntervals(aggDataType = aggDataType,
                                      timeColumnName = timeColumnName)[-1]


    def unaggregatedEndpoints(self, dataType = '', aggDataType = '',
                              timeColumnName = '', idColumnName = ''):
        """
        Sorted (ascending) endpoints and their IDs, if available,
        for unaggregated intervals since the last aggregation endpoint for a
        given data type.

        This has a problem where an endpoint at 23:45:04 will be returned as
        23:45:00. This makes the return value incorrect for raw data types
        having readings at sub-minute intervals such as data for circuit,
        irradiance and weather. This condition does not affect correct
        aggregation. Only the definition of the return value is wrong.

        :param dataType: string
        :param aggDataType: string
        :param timeColumnName: string
        :param idColName: string
        :return: list of datetimes.
        """

        if idColumnName != '':
            # Key:
            # 0: raw
            # 1: agg
            # 2: time col
            # 3: id col
            # 4: last aggregated time
            sql = 'SELECT "{0}".{2}, "{0}".{3} FROM "{0}" LEFT JOIN "{1}" ON ' \
                  '"{0}".{2} = "{1}".{2} AND "{0}".{3} = "{1}".{3} WHERE "{' \
                  '1}".{2} IS NULL AND "{0}".{2} > \'{4}\' ORDER BY {2} ASC, ' \
                  '{3} ASC'

            self.logger.log('last agg endpoint: {}'.format(
                self.lastAggregationEndpoint(aggDataType, timeColumnName)))

            # The id column value is available in the tuple returned by
            # groupby but is not being used here.

            # @todo Exclude last endpoint if it is equal to the last
            # aggregation endpoint.
            #
            # The minute position filtering may be including the last
            # endpoint incorrectly because there are readings occurring
            # within the same minute as the final endpoint, e.g. 23:45:04,
            # 23:45:08, etc.
            #
            # This is not a problem with eGuage data due reading intervals
            # being every minute and zero seconds.

            return map(lambda x: datetime(x[0], x[1], x[2], x[3], x[4], 0),
                       [k for k, v in groupby(
                           map(lambda y: y[0].timetuple()[0:5], filter(
                               lambda x: x[0].timetuple()[
                                             MINUTE_POSITION] %
                                         INTERVAL_DURATION == 0,
                               [(x[0], x[1]) for x in self.rows(
                                   sql.format(self.tables[dataType],
                                              self.tables[aggDataType],
                                              timeColumnName, idColumnName,
                                              self.lastAggregationEndpoint(
                                                  aggDataType,
                                                  timeColumnName)))])))])
        else:
            # Key:
            # 0: raw
            # 1: agg
            # 2: time col
            # 3: last aggregated time
            sql = 'SELECT "{0}".{2} FROM "{0}" LEFT JOIN "{1}" ON "{0}".{2}=' \
                  '"{1}".{2} WHERE "{1}".{2} IS NULL AND "{0}".{2} > \'{3}\' ' \
                  'ORDER BY {2} ASC'

            self.logger.log('last agg endpoint: {}'.format(
                self.lastAggregationEndpoint(aggDataType, timeColumnName)))

            return map(lambda x: datetime(x[0], x[1], x[2], x[3], x[4], 0),
                       [k for k, v in groupby(map(lambda y: y.timetuple()[0:5],
                                                  filter(
                                                      lambda x: x.timetuple()[
                                                                    MINUTE_POSITION] % INTERVAL_DURATION == 0,
                                                      [(x[0]) for x in
                                                       self.rows(sql.format(
                                                           self.tables[
                                                               dataType],
                                                           self.tables[
                                                               aggDataType],
                                                           timeColumnName,
                                                           self.lastAggregationEndpoint(
                                                               aggDataType,
                                                               timeColumnName)))])))])

    def intervalCrossed(self, minute = None, subkey = None):
        """
        Determine interval crossing. Intervals are at 0, 15, 45, 60 min.
        The interval size is determined by MECO source data.

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
        Rows from a SQL fetch.

        :param sql: Command to be executed.
        :returns: DB result set.
        """

        self.logger.log('sql: {}'.format(sql), 'debug')
        self.dbUtil.executeSQL(self.cursor, sql)
        return self.cursor.fetchall()


    def rawData(self, dataType = '', orderBy = None, timestampCol = '',
                startDate = '', endDate = ''):
        """
        Raw data to be aggregated.

        :param dataType: string
        :param orderBy: list
        :param timestampCol: string
        :param startDate: string
        :param endDate: string
        :returns: DB rows.
        """

        # @todo Validate args.

        orderBy = filter(None, orderBy)

        return self.rows("""SELECT {} FROM "{}" WHERE {} BETWEEN '{}' AND
        '{}' ORDER BY {}""".format(self.columns[dataType],
                                   self.tables[dataType], timestampCol,
                                   startDate, endDate, ','.join(orderBy)))


    def subkeys(self, dataType = '', timestampCol = '', subkeyCol = '',
                startDate = '', endDate = ''):
        """
        The distinct subkeys for a given data type within a time range.

        Subkeys are fields such as egauge_id in eGauge data or sensor_id in
        irradiance data.

        :param dataType: string
        :param timestampCol: string
        :param subkeyCol: string
        :param startDate: string
        :param endDate: string
        :returns: List of subkeys
        """

        return [sk[0] for sk in self.rows("""SELECT DISTINCT({}) FROM "{}"
        WHERE {} BETWEEN '{}' AND '{}'
            ORDER BY {}""".format(subkeyCol, self.tables[dataType],
                                  timestampCol, startDate, endDate, subkeyCol))]


    def insertAggregatedData(self, agg = None):
        """
        :param agg: MSGAggregatedData
        :return: None
        """

        if not agg.columns:
            raise Exception('agg columns not defined.')
        if not agg.data:
            raise Exception('agg data not defined.')

        self.logger.log('agg data: {}'.format(agg.data))
        self.logger.log('agg data type: {}'.format(type(agg.data)))

        def __insertData(values = ''):
            """
            Perform insert of data to the database using the given values.
            :param values: String containing values to be inserted.
            :return Nothing.
            """
            success = True
            sql = 'INSERT INTO "{0}" ({1}) VALUES( {2})'.format(
                self.tables[agg.aggregationType], ','.join(agg.columns), values)
            self.logger.log('sql: {}'.format(sql), 'debug')
            success = self.dbUtil.executeSQL(self.cursor, sql,
                                             exitOnFail = self.exitOnError)
            if self.commitOnEveryInsert:
                self.conn.commit()
            if not success and self.exitOnError:
                raise Exception('Failure during aggregated data insert.')


        for row in agg.data:
            if type(row) == type({}):
                # self.logger.log('row=%s' % row, 'debug')
                # self.logger.log('row type: %s' % type(row))

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
                        if valCnt < len(agg.columns) - 1:
                            values += ","
                        valCnt += 1
                    __insertData(values = values)

            elif type(row) == type([]):
                values = ''
                valCnt = 0
                for val in row:
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
                    if valCnt < len(agg.columns) - 1:
                        values += ","
                    valCnt += 1
                __insertData(values = values)
            else:
                self.logger.log('row = {}'.format(row), 'error')
                raise Exception('Row type not matched.')

        # End for row.
        self.conn.commit()


    def intervalAverages(self, sums, cnts, timestamp, timestampIndex,
                         subkeyIndex = None, subkey = None):
        """
        Aggregates all data for the current interval for the given subkey.

        For the case where there are no subkeys, subkeyIndex and subkey
        should be None.

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

            self.logger.log('key: {}'.format(subkey), 'debug')
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
                                'Aggregating {} rows of data.'.format(
                                    cnts[subkey][sumIndex]), 'debug')
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
                                'Aggregating {} rows of data.'.format(
                                    cnts[sumIndex]), 'debug')
                            reportedAgg = True
                        myAvgs.append(s / cnts[sumIndex])
                    else:
                        myAvgs.append('NULL')
                sumIndex += 1
            return myAvgs


    def dataParameters(self, dataType = ''):
        """
        Parameters for a given data type.
        :param dataType: string
        :return: (aggType, timeColName, subkeyColName)
        """
        try:
            assert len(self.dataParams[dataType]) == 3
            return self.dataParams[dataType]
        except:
            self.logger.log('Unmatched data type {}.'.format(dataType))


    def aggregateAllData(self, dataType = ''):
        """
        Convenience method for aggregating all data for a given data type.
        Data is inserted to individual aggregated data tables.
        :param dataType: String in the list of raw data types.
        :return: Nothing.
        """
        (aggType, timeColName, subkeyColName) = self.dataParameters(dataType)

        for start, end in self.monthStartsAndEnds(timeColumnName = timeColName,
                                                  dataType = dataType):
            self.logger.log('start, end: {}, {}'.format(start, end))
            aggData = self.aggregatedData(dataType = dataType,
                                          aggregationType = aggType,
                                          timeColumnName = timeColName,
                                          subkeyColumnName = subkeyColName,
                                          startDate = start.strftime(
                                              '%Y-%m-%d %H:%M:%S'),
                                          endDate = end.strftime(
                                              '%Y-%m-%d %H:%M:%S'))
            self.insertAggregatedData(agg = aggData)
            for row in aggData.data:
                self.logger.log('aggData row: {}'.format(row))


    def aggregateNewData(self, dataType = ''):
        """
        Convenience method for aggregating new data.

        :param dataType:
        :return: dict of {dataType: count of aggregation endpoints}
        """

        # The new aggregation starting point is equal to the last aggregation
        # endpoint up to the last unaggregated endpoint.

        (aggType, timeColName, subkeyColName) = self.dataParameters(dataType)

        (end, start) = \
            self.lastUnaggregatedAndAggregatedEndpoints(dataType).items()[0][1]

        self.logger.log(
            'datatype: {}; start, end: {}, {}; end type: {}'.format(dataType,
                                                                    start, end,
                                                                    type(end)),
            'critical')

        if type(end) == type(None):
            # No available unaggregated endpoints results in an empty list
            # for type egauge. The reason this does not work for other types is
            # because the other types of fractional minute readings and the
            # fractional minute readings are not being handled completely but
            # this method is still capable of working without problem.
            self.logger.log('Nothing to aggregate.')
            return {dataType: 0}

        if self.incrementEndpoint(start) >= end:
            self.logger.log('Nothing to aggregate.')
            return {dataType: 0}

        aggData = self.aggregatedData(dataType = dataType,
                                      aggregationType = aggType,
                                      timeColumnName = timeColName,
                                      subkeyColumnName = subkeyColName,
                                      startDate = self.incrementEndpoint(
                                          start).strftime('%Y-%m-%d %H:%M:%S'),
                                      endDate = end.strftime(
                                          '%Y-%m-%d %H:%M:%S'))
        self.insertAggregatedData(agg = aggData)
        for row in aggData.data:
            self.logger.log('aggData row: {}'.format(row))

        self.logger.log(
            '{} rows aggregated for {}.'.format(len(aggData.data), dataType))
        return {dataType: len(aggData.data)}

    def incrementEndpoint(self, endpoint = None):
        """
        Increment an endpoint by one interval where endpoints are the final
        timestamp in an aggregation interval.
        :param endpoint: the endpoint to be incremented.
        :return: datetime object that is the given endpoint + a predefined
        amount of minutes.
        """
        plusOneInterval = relativedelta(minutes = 15)
        return endpoint + plusOneInterval


    def lastUnaggregatedAndAggregatedEndpoints(self, dataType = ''):
        """
        Return the endpoints for the given data type in the form

        {datatype: (last unaggregated endpoint, last aggregated endpoint)}.
        :param dataType:
        :return: dict with tuple.
        """
        self.logger.log('datatype {}'.format(dataType))
        (aggType, timeColName, subkeyColName) = self.dataParameters(dataType)
        self.logger.log('subkey colname {}'.format(subkeyColName))

        unAggregatedEndpoints = self.unaggregatedEndpoints(dataType = dataType,
                                                           aggDataType =
                                                           aggType,
                                                           timeColumnName =
                                                           timeColName,
                                                           idColumnName =
                                                           subkeyColName)

        self.logger.log('unagg endpoints: {}'.format(unAggregatedEndpoints))
        return {dataType: (
            unAggregatedEndpoints[-1] if unAggregatedEndpoints != [] else None,
            self.lastAggregationEndpoint(aggDataType = aggType,
                                         timeColumnName = timeColName))}

    def aggregatedVsNewData(self):
        """
        Convenience method.
        :return: dict of tuples containing {datatype:(last raw datetime,
        last agg datetime)}
        """
        return {x.keys()[0]: (x.values()[0]) for x in
                map(self.lastUnaggregatedAndAggregatedEndpoints,
                    [k for k in self.dataParams])}


    def monthStartsAndEnds(self, timeColumnName = '', dataType = ''):
        """
        Return first date and last date for the given **raw** data type for each
        month in the data's entire time range.

        The end date is incremented by on aggregation period to account for
        the data obtained at time 00:00.

        :param timeColumnName: string
        :param dataType: string
        :return: List of tuples.
        """

        self.logger.log('datatype {}'.format(dataType), 'debug')
        (start, end) = self.rows(
            """SELECT MIN({}), MAX({}) FROM \"{}\"""".format(timeColumnName,
                                                             timeColumnName,
                                                             self.tables[
                                                                 dataType]))[0]
        self.logger.log('start {}'.format(start))
        self.logger.log('end {}'.format(end))

        # End time needs transforming in split dates to extend the end of the
        # day to 23:59:59.

        splitDates = self.timeUtil.splitDates(start, end)

        startEndDatesTransform = []
        i = 0
        while i < len(splitDates):
            startEndDatesTransform.append((splitDates[i][0],
                                           self.incrementEndpoint(datetime(
                                               splitDates[i][1].timetuple()[0],
                                               splitDates[i][1].timetuple()[1],
                                               splitDates[i][1].timetuple()[2],
                                               23, 59, 59))))
            i += 1

        return startEndDatesTransform


    def aggregatedData(self, dataType = '', aggregationType = '',
                       timeColumnName = '', subkeyColumnName = '',
                       startDate = '', endDate = ''):
        """
        ***********************************************************************
        Provide aggregated data.
        ***********************************************************************

        Start and end dates are used to calculate interval crossings.

        :param dataType: String
        :param aggregationType: String
        :param timeColumnName: String
        :param subkeyColumnName: String
        :param startDate: String
        :param endDate: String
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

        self.logger.log('subkeys: {}'.format(mySubkeys), 'debug')

        def __initSumAndCount(subkey = None, sums = None, cnts = None):
            """
            Initialize the sum and cnt data structures.
            :param subkey: string
            :param sums: list | dict | None
            :param cnts: list | dict | None
            """

            if not sums and not cnts:
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
                    sums[subkey] = []
                    for i in range(len(self.columns[dataType].split(','))):
                        sums[subkey].append(0)
                    cnts[subkey] = []
                    for i in range(len(self.columns[dataType].split(','))):
                        cnts[subkey].append(0)

            return (sums, cnts)

        (sum, cnt) = __initSumAndCount()


        def __initIntervalCrossings():
            """
            Perform initialization of the interval crossings used to
            determine when interval crossings occur.
            :returns None
            """

            subkeysToCheck = copy.copy(mySubkeys)
            self.logger.log('subkeys to check: {}'.format(subkeysToCheck),
                            'debug')

            if mySubkeys:
                for row in self.rawData(dataType = dataType,
                                        orderBy = [timeColumnName,
                                                   subkeyColumnName],
                                        timestampCol = timeColumnName,
                                        startDate = startDate,
                                        endDate = endDate):

                    # @CRITICAL: Exit after every subkey has been visited.
                    # This scans the raw data until each subkey is encountered
                    # ONCE and then exits.
                    if subkeysToCheck != []:
                        if row[ci(subkeyColumnName)] in subkeysToCheck:
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
                        self.logger.log('next min crossing for {} = {}'.format(
                            row[ci(subkeyColumnName)],
                            self.nextMinuteCrossing[row[ci(subkeyColumnName)]]),
                                        'debug')
                    else:
                        break

            else:
                # Non-subkey case e.g. weather data.
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
                    self.logger.log('next min crossing = {}'.format(
                        self.nextMinuteCrossingWithoutSubkeys), 'debug')
                    rowCnt += 1
                    if rowCnt > 0:
                        break

        __initIntervalCrossings()

        for row in self.rawData(dataType = dataType,
                                orderBy = [timeColumnName, subkeyColumnName],
                                timestampCol = timeColumnName,
                                startDate = startDate, endDate = endDate):

            if mySubkeys:
                for col in self.columns[dataType].split(','):
                    if self.mathUtil.isNumber(row[ci(col)]) and ci(col) != ci(
                            subkeyColumnName):
                        sum[row[ci(subkeyColumnName)]][ci(col)] += row[ci(col)]
                        cnt[row[ci(subkeyColumnName)]][ci(col)] += 1

                minute = row[ci(timeColumnName)].timetuple()[MINUTE_POSITION]

                if self.intervalCrossed(minute = minute,
                                        subkey = row[ci(subkeyColumnName)]):
                    minuteCrossed = minute

                    # Perform aggregation on all of the previous data including
                    # the current data for the current subkey.
                    self.logger.log('key: {}'.format(row[ci(subkeyColumnName)]),
                                    'debug')
                    aggData += [
                        self.intervalAverages(sum, cnt, row[ci(timeColumnName)],
                                              ci(timeColumnName),
                                              ci(subkeyColumnName),
                                              row[ci(subkeyColumnName)])]
                    self.logger.log('minute crossed {}'.format(minuteCrossed),
                                    'DEBUG')

                    # Init current sum and cnt for subkey that has a completed
                    # interval.
                    (sum, cnt) = __initSumAndCount(
                        subkey = row[ci(subkeyColumnName)], sums = sum,
                        cnts = cnt)
            else:
                for col in self.columns[dataType].split(','):
                    if self.mathUtil.isNumber(row[ci(col)]):
                        sum[ci(col)] += row[ci(col)]
                        cnt[ci(col)] += 1

                minute = row[ci(timeColumnName)].timetuple()[MINUTE_POSITION]

                if self.intervalCrossed(minute = minute):
                    aggData += [
                        self.intervalAverages(sum, cnt, row[ci(timeColumnName)],
                                              ci(timeColumnName))]
                    (sum, cnt) = __initSumAndCount(subkey = None, sums = sum,
                                                   cnts = cnt)

            rowCnt += 1

        self.logger.log('aggdata = {}'.format(aggData), 'debug')
        return MSGAggregatedData(aggregationType = aggregationType,
                                 columns = self.columns[dataType].split(','),
                                 data = aggData)
