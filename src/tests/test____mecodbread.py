#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'

import unittest
from mecodbread import MECODBReader
from mecodbconnect import MECODBConnector
from mecodbinsert import MECODBInserter
from mecodbutils import MECODBUtil
from meco_dbdelete import MECODBDeleter


class TestMECODBRead(unittest.TestCase):
    def setUp(self):
        self.reader = MECODBReader()
        self.connector = MECODBConnector(True)
        self.conn = self.connector.connectDB()
        self.inserter = MECODBInserter()
        self.util = MECODBUtil()
        self.lastSeqVal = None
        self.tableName = 'MeterData'
        self.colName = 'meter_data_id'
        self.deleter = MECODBDeleter()

    def testMECODBReadCanBeInited(self):
        self.assertIsNotNone(self.reader)

    def testSelectRecord(self):
        """Insert and retrieve a record to test the ability to select a record.
        """

        print "testSelectRecord:"
        print "self.conn = %s" % self.conn

        sampleDict = {'MeterName': '100001', 'UtilDeviceID': '100001',
                      'MacID': '00:00:00:00:00:00:00:00'}
        self.inserter.insertData(self.conn, self.tableName, sampleDict)
        self.lastSeqVal = self.util.getLastSequenceID(self.conn, self.tableName,
                                                      self.colName)

        print "lastSeqVal = %s" % self.lastSeqVal

        row = self.reader.selectRecord(self.conn, self.tableName, self.colName,
                                       self.lastSeqVal)
        self.assertEqual(row[self.colName], self.lastSeqVal)

    def tearDown(self):
        # delete the record that was inserted
        if self.lastSeqVal != None:
            self.deleter.deleteRecord(self.conn, self.tableName, self.colName,
                                      self.lastSeqVal)

        self.connector.closeDB(self.conn)

if __name__ == '__main__':
    unittest.main()
