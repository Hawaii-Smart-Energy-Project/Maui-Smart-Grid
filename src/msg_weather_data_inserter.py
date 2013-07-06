#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'

from msg_weather_data_dupe_checker import MSGWeatherDataDupeChecker
# from msg_weather_data_mapper import MSGWeatherDataMapper
from mecodbutils import MECODBUtil
from msg_logger import MSGLogger


class MSGNOAAWeatherDataInserter(object):
    """
    Performs weather data insertion to the database.
    """

    def __init__(self):
        """
        Constructor.
        """

        self.logger = MSGLogger(__name__, 'info')
        self.dbUtil = MECODBUtil()
        self.dupeChecker = MSGWeatherDataDupeChecker()
        # self.mapper = MSGWeatherDataMapper()

    def insertDataDict(self, conn, tableName, listOfDataDicts, fKeyVal = None,
                       withoutCommit = 0):
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

            # self.dbUtil.executeSQL(cur, sql)
            print sql

            if withoutCommit == 0:
                try:
                    # conn.commit()
                    pass
                except:
                    # self.logger.log("ERROR: Commit failed.", 'debug')

                    # return cur
                    pass

