#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'

from msg_weather_data_dupe_checker import MSGWeatherDataDupeChecker
# from msg_weather_data_mapper import MSGWeatherDataMapper
from mecodbutils import MECODBUtil
from msg_logger import MSGLogger
import sys

class MSGNOAAWeatherDataInserter(object):
    """
    Performs weather data insertion to a database.
    """

    def __init__(self, testing = False):
        """
        Constructor.
        :param testing: True if testing mode is being used.
        """

        self.logger = MSGLogger(__name__, 'info')
        self.dbUtil = MECODBUtil()
        self.dupeChecker = MSGWeatherDataDupeChecker()
        # self.mapper = MSGWeatherDataMapper()

    def insertDataDict(self, conn, tableName, listOfDataDicts, fKeyVal = None,
                       commit = False):
        """
        Given a table name and a dictionary of column names and values,
        insert them to the db.

        :param conn: database connection
        :param tableName: name of the db table
        :param columnsAndValues: dictionary of columns and values to be
        inserted to the db
        :param (optional) fKeyVal: an explicit foreign key value
        :param (optional) withoutCommit: a flag indicated that the insert
        will not be immediately committed
        :returns: A database cursor.
        """

        cur = conn.cursor()

        for row in listOfDataDicts:

            # Get a dictionary of mapped (from DB to source data) column names.
            # columnDict = self.mapper.getDBColNameDict(tableName)

            # dbColsAndVals = {}

            # Add a creation timestamp using the SQL function.
            row['created'] = 'NOW()'

            cols = []
            vals = []


            for col in row.keys():
                # Prepare the columns and values for insertion via SQL.


                cols.append(col)
                if (row[col] != 'NULL'):
                    # Surround value with single quotes.
                    vals.append("'%s'" % row[col])
                else:
                    # Except for NULL values.
                    vals.append("%s" % row[col])

            sql = 'insert into "' + tableName + '" (' + ','.join(
                cols) + ')' + ' values (' + ','.join(vals) + ')'

            if self.dbUtil.executeSQL(cur, sql, exitOnFail = False) is False:
                for col in sorted(row.keys()):
                    print "%s: %s" % (col,row[col])
                sys.exit(-1)

            # self.logger.log("sql = %s" % sql, 'debug')

            if commit:
                try:
                    conn.commit()
                except:
                    self.logger.log("ERROR: Commit failed.", 'debug')


