#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'

class MECODupeChecker(object) :
    """Check for duplicate data in the database.
    """

    def __init__(self) :
        """Constructor
        """
        pass

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
	                    "Reading".channel
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
            print "Found %s existing matches." % len(rows)
            return True
        else:
            return False
