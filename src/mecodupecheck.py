#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'

from mecodbconnect import MECODBConnector

class MECODupeChecker(object) :
    """Check for duplicate data in the database.
    """

    def __init__(self) :
        """Constructor
        """
        self.connector = MECODBConnector()
        self.conn = self.connector.connectDB()
        self.cur = self.conn.cursor()

    def meterIDAndEndTimeExists(self, meterName, endTime):
        """Check if the meterID and endTime combination exists in the database.
        :param meterID: Meter name in MeterData table
        :param endTime: End time in Interval table
        :return True if combo exists, False if not.
        """
        sql = """SELECT	"Interval".end_time,
                        "MeterData".meter_name,
	                    "MeterData".meter_data_id
                 FROM "MeterData"
                 INNER JOIN "IntervalReadData" ON "MeterData".meter_data_id = "IntervalReadData".meter_data_id
                 INNER JOIN "Interval" ON "IntervalReadData".interval_read_data_id = "Interval".interval_read_data_id
                 WHERE "Interval".end_time = '%s' and meter_name = '%s'""" % (endTime, meterName)

        result = None
        try :
            result = self.cur.execute(sql)
        except Exception, e :
            print "Execute failed with " + sql
            print "ERROR: ", e[0]
            print

        rows = self.cur.fetchall()

        if len(rows) > 0:
            print "Found %s existing matches." % len(rows)
            return True
        else:
            return False
