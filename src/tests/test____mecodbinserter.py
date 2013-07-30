#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'

import unittest
from meco_db_insert import MECODBInserter
from msg_db_util import MSGDBUtil
from meco_db_connector import MSGDBConnector
from meco_db_delete import MECODBDeleter
from meco_db_read import MECODBReader


class TestMECODBInserter(unittest.TestCase):
    """
    Unit tests for the MECO XML Parser.
    """

    def setUp(self):
        self.i = MECODBInserter()
        self.util = MSGDBUtil()
        self.connector = MSGDBConnector(True)
        self.deleter = MECODBDeleter()
        self.reader = MECODBReader()
        self.lastSeqVal = None
        self.conn = self.connector.connectDB()
        self.sampleTableName = 'MeterData'
        self.sampleDict = {'MeterName': '100001', 'UtilDeviceID': '100001',
                           'MacID': '00:00:00:00:00:00:00:00'}
        self.keyName = 'meter_data_id'

    def testMECODBInserterCanBeInited(self):
        localInserter = MECODBInserter()
        self.assertIsInstance(self.i, type(localInserter))

    def testInsertionToMeterDataTable(self):
        """Data can be written to the Meter Data table.
        """

        # Insert some values.
        self.i.insertData(self.conn, self.sampleTableName, self.sampleDict)

        # Retrieve the last fetched value.
        self.lastSeqVal = self.util.getLastSequenceID(self.conn,
                                                      self.sampleTableName,
                                                      self.keyName)

        print "lastSeqVal = %s" % self.lastSeqVal

        row = self.reader.selectRecord(self.conn, self.sampleTableName,
                                       self.keyName, self.lastSeqVal)
        self.assertEqual(row[self.keyName], self.lastSeqVal)

    def test_fkey_value_is_correct(self):
        """Verify that the fkey value used during insertion is correct.
        """

    def tearDown(self):
        # Delete the record that was inserted.
        if self.lastSeqVal != None:
            self.deleter.deleteRecord(self.conn, self.sampleTableName,
                                      self.keyName, self.lastSeqVal)

        self.connector.closeDB(self.conn)

if __name__ == '__main__':
    unittest.main()
