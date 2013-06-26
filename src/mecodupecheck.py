#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'

from mecoconfig import MECOConfiger
from mecodbutils import MECODBUtil
from mecologger import MECOLogger


class MECODupeChecker(object):
    """
    Check for duplicate data in the database.
    """

    def __init__(self):
        """
        Constructor.
        """

        self.logger = MECOLogger(__name__, 'debug')
        self.mecoConfig = MECOConfiger()
        self.currentReadingID = 0
        self.dbUtil = MECODBUtil()


    def getLastElement(self, rows):
        """
        Get the last element in a collection.

        Example:
            rows = (element1, element2, element3)
            getLastElement(rows) # return element3

        :param rows Result froms from a query
        :return last element in the collection
        """

        for i, var in enumerate(rows):
            if i == len(rows) - 1:
                return var

    def registerBranchDupeExists(self, conn, meterName, readTime,
                                 registerNumber, DEBUG = False):
        """
        Determine if a register branch duplicate exists for a given meter
        name, read time, number tuple.

        :param conn: Database connection.
        :param meterName: Meter name in MeterData table.
        :param readTime: Read time in RegisterRead table.
        :param registerNumber: Corresponds to DB column "number".
        :return: True if tuple exists, False if not.
        """

        dbCursor = conn.cursor()

        sql = """SELECT "public"."MeterData".meter_name,
                        "public"."RegisterRead".read_time,
                        "public"."Register"."number"
                 FROM "public"."MeterData"
                 INNER JOIN "public"."RegisterData" ON
                      "public" ."MeterData".meter_data_id = "public"
                      ."RegisterData".meter_data_id
                 INNER JOIN "public"."RegisterRead" ON
                      "public"."RegisterData" .register_data_id = "public"
                      ."RegisterRead".register_data_id
                 INNER JOIN "public"."Tier" ON "public"."RegisterRead"
                 .register_read_id = "public"."Tier" .register_read_id
                 INNER JOIN "public"."Register" ON "public"."Tier".tier_id =
                 "public"."Register".tier_id
                 WHERE "public"."MeterData".meter_name = '%s'
                 AND "public"."RegisterRead".read_time = '%s'
                 AND "public"."Register".number = '%s'
                 """ % (meterName, readTime, registerNumber)

        self.dbUtil.executeSQL(dbCursor, sql)
        rows = dbCursor.fetchall()

        if len(rows) > 0:
            return True
        else:
            return False


    def readingBranchDupeExists(self, conn, meterName, endTime, channel = None,
                                DEBUG = False):
        """
        Duplicate cases:
        1. meterID and endTime combination exists in the database.
            @deprecated in favor of full meterName-endTime-channel query

        2. meterID, endTime, channel combination exists in the database.

        :param conn: Database connection.
        :param meterName: Meter name in MeterData table.
        :param endTime: End time in Interval table.
        :param channel: Required parameter that was previously optional. An
        optional channel is now deprecated.
        :return: True if tuple exists, False if not.
        """

        dbCursor = conn.cursor()

        if DEBUG:
            print "readingBranchDupeExists():"

        if channel != None:
            sql = """SELECT	"Interval".end_time,
                            "MeterData".meter_name,
                            "MeterData".meter_data_id,
                            "Reading".channel,
                            "Reading".reading_id
                     FROM "MeterData"
                     INNER JOIN "IntervalReadData" ON "MeterData"
                     .meter_data_id =
                      "IntervalReadData".meter_data_id
                     INNER JOIN "Interval" ON "IntervalReadData"
                     .interval_read_data_id = "Interval".interval_read_data_id
                     INNER JOIN "Reading" ON "Interval".interval_id = "Reading"
                     .interval_id
                     WHERE "Interval".end_time = '%s' and meter_name = '%s' and
                     channel = '%s'""" % (
                endTime, meterName, channel)

        else: # deprecated query
            sql = """SELECT	"Interval".end_time,
                            "MeterData".meter_name,
                            "MeterData".meter_data_id
                     FROM "MeterData"
                     INNER JOIN "IntervalReadData" ON "MeterData"
                     .meter_data_id =
                      "IntervalReadData".meter_data_id
                     INNER JOIN "Interval" ON "IntervalReadData"
                     .interval_read_data_id = "Interval".interval_read_data_id
                     WHERE "Interval".end_time = '%s' and meter_name =
                     '%s'""" % (
                endTime, meterName)

        self.dbUtil.executeSQL(dbCursor, sql)
        rows = dbCursor.fetchall()

        if len(rows) > 0:
            assert len(
                rows) < 2, "Dupes should be less than 2, found %s: %s." % (
                len(rows), rows)

            self.currentReadingID = self.getLastElement(rows[0])
            self.logger.log('Reading ID = %s.' % self.currentReadingID,
                            'silent')

            self.logger.log(
                "Duplicate found for meter %s, end time %s, channel %s." % (
                    meterName, endTime, channel), 'silent')
            return True

        else:
            self.logger.log(
                "Found no rows for meter %s, end time %s, channel %s." % (
                    meterName, endTime, channel), 'silent')
            return False


    def readingValuesAreInTheDatabase(self, conn, readingDataDict):
        """
        Given a reading ID, verify that the values associated are present
        in the database.

        Values are from the columns:
            1. channel
            2. raw_value
            3. uom
            4. value

        :param dictionary containing reading values
        :return True if the existing values are the same, otherwise return False
        """

        dbCursor = conn.cursor()

        sql = """SELECT "Reading".reading_id,
                                "Reading".channel,
                                "Reading".raw_value,
                                "Reading".uom,
                                "Reading"."value"
                         FROM "Reading"
                         WHERE "Reading".reading_id = %s""" % (
            self.currentReadingID)

        self.dbUtil.executeSQL(dbCursor, sql)
        rows = dbCursor.fetchall()

        if self.currentReadingID == 0:
            return False

        # assert len(rows) == 1 or len(rows) == 0
        assert len(
            rows) == 1, "Didn't find a matching reading for reading ID %s." % \
                        self.currentReadingID
        if len(rows) == 1:
            self.logger.log("Found %s existing matches." % len(rows), 'silent')

            allEqual = True
            if int(readingDataDict['Channel']) == int(rows[0][1]):
                print "channel equal,"
            else:
                self.logger.log("channel not equal: %s,%s,%s" % (
                    int(readingDataDict['Channel']), int(rows[0][1]),
                    readingDataDict['Channel'] == rows[0][1]), 'debug')
                allEqual = False

            if int(readingDataDict['RawValue']) == int(rows[0][2]):
                print "raw value equal,"
            else:
                self.logger.log("rawvalue not equal: %s,%s,%s" % (
                    int(readingDataDict['RawValue']), int(rows[0][2]),
                    readingDataDict['RawValue'] == rows[0][2]), 'debug')
                allEqual = False

            if readingDataDict['UOM'] == rows[0][3]:
                print "uom equal,"
            else:
                self.logger.log("uom not equal: %s,%s,%s" % (
                    readingDataDict['UOM'], rows[0][3],
                    readingDataDict['UOM'] == rows[0][3]), 'debug')
                allEqual = False

            if self.approximatelyEqual(float(readingDataDict['Value']),
                                       float(rows[0][4]), 0.001):
                self.logger.log("value equal", 'silent')
            else:
                self.logger.log("value not equal: %s,%s,%s" % (
                    float(readingDataDict['Value']), float(rows[0][4]),
                    readingDataDict['Value'] == rows[0][4]), 'debug')
                allEqual = False

            if allEqual:
                return True
            else:
                return False
        else:
            return False


    def approximatelyEqual(self, a, b, tolerance):
        return abs(a - b) < tolerance

