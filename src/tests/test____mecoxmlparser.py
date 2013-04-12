#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'

import unittest
from mecoxmlparser import MECOXMLParser
from mecodbconnect import MECODBConnector
from mecodbutils import MECODBUtil


class TestMECOXMLParser(unittest.TestCase):
    """Unit tests for MECO XML Parser.
    """

    def setUp(self):
        self.p = MECOXMLParser(True) # run in testing mode
        self.dbConnect = MECODBConnector(True)
        self.dbUtil = MECODBUtil()
        self.conn = self.dbConnect.connectDB()
        self.cur = self.conn.cursor()
        # self.dbUtil.eraseTestMeco(self.cur)

    def _testMECOXMLParserCanBeInited(self):
        self.assertIsNotNone(self.p)

    def testEveryElementIsVisited(self):
        self.dbUtil.eraseTestMeco(self.cur)
        self.conn.commit()
        self.p.filename = "../../test-data/meco-energy-test-data.xml"
        fileObject = open(self.p.filename, "rb")
        expectedCount = 656
        self.p.parseXML(fileObject, True)
        print "element count = %s" % self.p.elementCount
        self.p.performRollback()
        self.assertEqual(self.p.elementCount, expectedCount)

    def _testAllTableNamesArePresent(self):
        self.p.filename = "../../test-data/meco-energy-test-data.xml"
        fileObject = open(self.p.filename, "rb")
        self.p.parseXML(fileObject, True)
        fail = 0

        for key in self.p.tableNameCount.keys():
            print key + ": ",
            print self.p.tableNameCount[key]

        for c in self.p.tableNameCount.values():
            if c < 1:
                fail = 1
        self.assertEqual(fail, 0)

    def tearDown(self):
        pass
        # self.dbUtil.eraseTestMeco(self.cur)


if __name__ == '__main__':
    unittest.main()
