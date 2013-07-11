#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'

from mecomapper import MECOMapper
from mecodupecheck import MECODupeChecker
from msg_db_util import MSGDBUtil
from msg_logger import MSGLogger

VISUALIZE_DATA = 1
DEBUG = 1


class MECODBInserter(object):
    """
    This provides methods that perform insertion of MECO data.
    """

    def __init__(self):
        """
        Constructor.
        """

        self.logger = MSGLogger(__name__, 'debug')
        self.mapper = MECOMapper()
        self.dupeChecker = MECODupeChecker()
        self.dbUtil = MSGDBUtil()

    def __call__(self, param):
        print "CallableClass.__call__(%s)" % param

    def insertData(self, conn, tableName, columnsAndValues, fKeyVal = None,
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

        # Get a dictionary of mapped (from DB to source data) column names.
        columnDict = self.mapper.getDBColNameDict(tableName)

        dbColsAndVals = {}

        if VISUALIZE_DATA:
            print "----------" + tableName + "----------"
            print columnDict
            print columnsAndValues

        for col in columnDict.keys():

            # Use default as the value for the primary key so that the
            # private key is obtained from the predefined sequence.
            if col == '_pkey':
                if VISUALIZE_DATA:
                    print columnDict[col], # db col name
                    print 'DEFAULT'
                dbColsAndVals[columnDict[col]] = 'DEFAULT'

            # For the foreign key, set the value from the given parameter.
            elif col == '_fkey':
                if VISUALIZE_DATA:
                    print columnDict[col], # db col name
                    print fKeyVal
                dbColsAndVals[columnDict[col]] = fKeyVal

            else:
                if VISUALIZE_DATA:
                    print columnDict[col], # db col name

                # The Register and Reading tables need to handle NULL
                # values as a special case.
                if tableName == 'Register' or tableName == 'Reading':
                    try:
                        if VISUALIZE_DATA:
                            print columnsAndValues[col] # data source value
                        dbColsAndVals[columnDict[col]] = columnsAndValues[col]
                    except:
                        if VISUALIZE_DATA:
                            print 'NULL'
                        dbColsAndVals[columnDict[col]] = 'NULL'

                # For all other cases, simply pass the value.
                else:
                    if VISUALIZE_DATA:
                        print columnsAndValues[col] # data source value
                    dbColsAndVals[columnDict[col]] = columnsAndValues[col]

        # Add a creation timestamp to MeterData.
        if tableName == 'MeterData':
            dbColsAndVals['created'] = 'NOW()'

        cols = []
        vals = []
        for col in dbColsAndVals.keys():
            cols.append(col)

            # DEFAULT, NULL and NOW() need to appear without quotes.
            if dbColsAndVals[col] in {'DEFAULT', 'NULL', 'NOW()'}:
                vals.append(dbColsAndVals[col])
            else:
                vals.append("'%s'" % dbColsAndVals[
                    col]) # surround value with single quotes

        sql = 'insert into "' + tableName + '" (' + ','.join(
            cols) + ')' + ' values (' + ','.join(
            vals) + ')'

        # if DEBUG:
        #     print "sql=" + sql

        self.dbUtil.executeSQL(cur, sql)

        if withoutCommit == 0:
            try:
                conn.commit()
            except:
                self.logger.log("ERROR: Commit failed.",'debug')

        return cur

