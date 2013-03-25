#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'

class MECODupeChecker(object) :
    """Check for duplicate data in the database.
    """

    def __init__(self) :
        """Constructor
        """
        self.currentReadingID = 0

    def readingBranchDupeExists(self, conn, meterName, endTime, channel=None):
        """
        Duplicate cases:
        1. meterID and endTime combination exists in the database.
        2. meterID, endTime, channel combination exists in the database.

        :param conn: database connection
        :param meterID: Meter name in MeterData table
        :param endTime: End time in Interval table
        :param channel: optional parameter
        :return True if combo exists, False if not.
        """

        dbCursor = conn.cursor()

        if channel != None:
            print "channel param = %s" % channel
            sql = """SELECT	"Interval".end_time,
                        "MeterData".meter_name,
	                    "MeterData".meter_data_id,
	                    "Reading".channel,
	                    "Reading".reading_id
                 FROM "MeterData"
                 INNER JOIN "IntervalReadData" ON "MeterData".meter_data_id = "IntervalReadData".meter_data_id
                 INNER JOIN "Interval" ON "IntervalReadData".interval_read_data_id = "Interval".interval_read_data_id
                 INNER JOIN "Reading" ON "Interval".interval_id = "Reading".interval_id
                 WHERE "Interval".end_time = '%s' and meter_name = '%s' and channel = '%s'""" % (endTime, meterName, channel)
        else:
            sql = """SELECT	"Interval".end_time,
                        "MeterData".meter_name,
	                    "MeterData".meter_data_id
                 FROM "MeterData"
                 INNER JOIN "IntervalReadData" ON "MeterData".meter_data_id = "IntervalReadData".meter_data_id
                 INNER JOIN "Interval" ON "IntervalReadData".interval_read_data_id = "Interval".interval_read_data_id
                 WHERE "Interval".end_time = '%s' and meter_name = '%s'""" % (endTime, meterName)

        result = None
        try :
            result = dbCursor.execute(sql)
        except Exception, e :
            print "Execute failed with " + sql
            print "ERROR: ", e[0]
            print

        rows = dbCursor.fetchall()

        if len(rows) > 0:
            assert len(rows) < 2 # dupes are dropped before insert, therefore,
                                 # there should never be more than two
            if channel and len(rows) == 1:
                print "Found %s existing matches in \"Reading\"." % len(rows)
                print "rows = ",
                print rows

                self.currentReadingID = self.getLastElement(rows[0])
                print "reading id = %s" % self.currentReadingID

            return True
        else:
            return False


    def getLastElement(self, rows):
        """Get the last element in a collection.

        Example:
            rows = (element1, element2, element3)
            getLastElement(rows) # return element3

        :param rows Result froms from a query
        :return last element in the collection
        """

        for i, var in enumerate(rows):
            if i == len(rows) - 1:
                return var


    def readingValuesAreInTheDatabase(self, conn, readingDataDict):
        """Given a reading ID, verify that the values associated are present in the database.
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
                 WHERE "Reading".reading_id = %s""" % (self.currentReadingID)

        result = None

        try :
            result = dbCursor.execute(sql)
        except Exception, e :
            print "Execute failed with " + sql
            print "ERROR: ", e[0]
            print
        rows = dbCursor.fetchall()

        assert len(rows) == 1 or len(rows) == 0
        if len(rows) == 1:
            print "Found %s existing matches." % len(rows)
            print "rows = %s" % rows

            print "dict:"
            for key in readingDataDict.keys():
                print key, readingDataDict[key]
            print "row:"
            index = 0
            for item in rows[0]:
                print "index %s: %s" % (index, item)
                index += 1

            # handle floating point 0 special case
            if readingDataDict['Value'] == 0 :
                readingDataDict['Value'] = '0.0'

            if readingDataDict['Channel'] == rows[0][0] and \
                readingDataDict['RawValue'] == rows[0][1] and \
                readingDataDict['UOM'] == rows[0][2] and \
                readingDataDict['Value'] == rows[0][3]:

                print "all are equal"
                return True
            else:
                print "all are NOT equal!"
                print rows[0][0], rows[0][1], rows[0][2], rows[0][3]
                return False
        else:
            return False
