#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'

from mecomapper import MECOMapper
from mecodupecheck import MECODupeChecker

VISUALIZE_DATA = 0
DEBUG = 0

class MECODBInserter(object) :
    """Provide data insertion methods for MECO data.
    """

    def __init__(self) :
        """Constructor
        """

        self.mapper = MECOMapper()
        self.dupeChecker = MECODupeChecker()

    def __call__(self, param) :
        print "CallableClass.__call__(%s)" % param

    def insertData(self, conn, tableName, columnsAndValues, fKeyVal = None, withoutCommit = 0) :
        """Given a table name and a dictionary of column names and values, insert them to the db.
        :param conn: database connection
        :param tableName: name of db table
        :param columnsAndValues dictionary: columns and values to be inserted to the db
        :returns: database cursor
        """

        cur = conn.cursor()
        columnDict = self.mapper.getDBColNameDict(
            tableName) # dict of mapped (from db to source data) column names
        dbColsAndVals = {}

        if VISUALIZE_DATA :
            print "----------" + tableName + "----------"
            print columnDict
            print columnsAndValues

        for col in columnDict.keys() :
            # use default as the value for the primary key
            # so that the private key is obtained from the predefined
            # sequence.
            if col == '_pkey' :
                if VISUALIZE_DATA :
                    print columnDict[col], # db col name
                    print 'DEFAULT'
                dbColsAndVals[columnDict[col]] = 'DEFAULT'

            # for the foreign key, set the value from the given parameter.
            elif col == '_fkey' :
                if VISUALIZE_DATA :
                    print columnDict[col], # db col name
                    print fKeyVal
                dbColsAndVals[columnDict[col]] = fKeyVal

            else :
                if VISUALIZE_DATA :
                    print columnDict[col], # db col name

                # the register and reading tables need to handle NULL
                # values as a special case.
                if tableName == 'Register' or tableName == 'Reading' :
                    try :
                        if VISUALIZE_DATA :
                            print columnsAndValues[col] # data source value
                        dbColsAndVals[columnDict[col]] = columnsAndValues[col]
                    except :
                        if VISUALIZE_DATA :
                            print 'NULL'
                        dbColsAndVals[columnDict[col]] = 'NULL'

                # for all other cases, simply pass the value.
                else :
                    if VISUALIZE_DATA :
                        print columnsAndValues[col] # data source value
                    dbColsAndVals[columnDict[col]] = columnsAndValues[col]

        cols = []
        vals = []
        for col in dbColsAndVals.keys() :
            cols.append(col)

            # DEFAULT and NULL need to appear without quotes.
            if dbColsAndVals[col] == 'DEFAULT' :
                vals.append(dbColsAndVals[col])
            elif dbColsAndVals[col] == 'NULL' :
                vals.append(dbColsAndVals[col])
            else :
                vals.append("'%s'" % dbColsAndVals[col])

        sql = 'insert into "' + tableName + '" (' + ','.join(cols) + ')' + ' values (' + ','.join(
            vals) + ')'

        if DEBUG :
            print "sql=" + sql

        try :
            cur.execute(sql)
        except Exception, e :
            print "execute failed with " + sql
            print "ERROR: ", e[0]
            print

        if withoutCommit == 0 :
            try :
                conn.commit()
                pass
            except :
                print "ERROR: Commit failed."

        return cur

