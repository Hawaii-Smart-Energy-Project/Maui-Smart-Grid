#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'

import unittest
from mecodbutils import MECODBUtil
from mecodbinsert import MECODBInserter
from mecodbconnect import MECODBConnector
from meco_dbdelete import MECODBDeleter

class TestMECODBUtil(unittest.TestCase) :
    """Unit tests for MECO DB Utils.
    """

    def setUp(self) :
        self.i = MECODBInserter()
        self.dbUtil = MECODBUtil()
        self.connector = MECODBConnector()
        self.conn = self.connector.connectDB()
        self.lastSeqVal = None
        self.dictCur = self.connector.dictCur # does this work? having the dictcur be in another class?
        self.deleter = MECODBDeleter()
        self.tableName = 'Testing_MeterData'
        self.columnName = 'meter_data_id'

    def testMECODBUtilCanBeInited(self) :
        self.assertIsNotNone(self.dbUtil)

    def testLastSequenceNumberIsCorrect(self) :
        """Test if last sequence ID value is generated correctly. Do this by inserting
        and deleting a DB record.
        """

        # insert some values
        sampleDict = {'MeterName' : '100001', 'UtilDeviceID' : '100001',
                      'MacID' : '00:00:00:00:00:00:00:00'}
        self.i.insertData(self.conn, self.tableName, sampleDict)


        self.lastSeqVal = self.dbUtil.getLastSequenceID(self.conn, self.tableName, self.columnName)
        print "lastSeqVal = %s" % self.lastSeqVal

        sql = "select * from \"%s\" where %s = %s" % (self.tableName, self.columnName, self.lastSeqVal)
        dictCur = self.connector.dictCur
        self.dbUtil.executeSQL(dictCur, sql)
        row = dictCur.fetchone()
        meterDataID = row[self.columnName]
        self.assertEqual(self.lastSeqVal, meterDataID)

    def tearDown(self) :
        """Delete the record that was inserted.
        """
        if self.lastSeqVal != None:
            self.deleter.deleteRecord(self.conn, self.tableName, self.columnName, self.lastSeqVal)

    if __name__ == '__main__' :
        unittest.main()
