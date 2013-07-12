#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'

import unittest
from meco_xml_parser import MECOXMLParser
from meco_db_connector import MSGDBConnector
from msg_db_util import MSGDBUtil


class TestMECOXMLParser(unittest.TestCase):
    """
    Unit tests for MECO XML Parser.
    """

    def setUp(self):
        self.p = MECOXMLParser(True) # run in testing mode
        self.dbConnect = MSGDBConnector(True)
        self.dbUtil = MSGDBUtil()
        self.conn = self.dbConnect.connectDB()
        self.cur = self.conn.cursor()

    def testMECOXMLParserCanBeInited(self):
        self.assertIsNotNone(self.p)

    def testEveryElementIsVisited(self):
        self.dbUtil.eraseTestMeco()

        self.p.filename = "../../test-data/meco_v3-energy-test-data.xml"
        fileObject = open(self.p.filename, "rb")
        expectedCount = 126
        self.p.parseXML(fileObject, True)
        print "element count = %s" % self.p.processForInsertElementCount
        self.assertEqual(self.p.processForInsertElementCount, expectedCount)

    def testAllTableNamesArePresent(self):
        self.dbUtil.eraseTestMeco()

        self.p.filename = "../../test-data/meco_v3-energy-test-data.xml"
        fileObject = open(self.p.filename, "rb")
        self.p.parseXML(fileObject, True)
        fail = False

        for key in self.p.tableNameCount.keys():
            print key + ": ",
            print self.p.tableNameCount[key]

            if self.p.tableNameCount[key] < 1:
                if key != 'ChannelStatus' and key != 'IntervalStatus' and key \
                        != 'EventData' and key != 'Event':
                    print "table = %s" % key
                    fail = True
        self.assertFalse(fail,
                         "At least one table of each type should have been "
                         "encountered.")

    def tearDown(self):
        self.dbConnect.closeDB(self.conn)

if __name__ == '__main__':
    unittest.main()
