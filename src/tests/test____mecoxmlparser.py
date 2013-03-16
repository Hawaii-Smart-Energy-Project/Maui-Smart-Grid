#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'

import unittest
from mecoxmlparser import MECOXMLParser

class TestMECOXMLParser(unittest.TestCase) :
    """Unit tests for MECO XML Parser.
    """

    def setUp(self) :
        self.p = MECOXMLParser()

    def testMECOXMLParserCanBeInited(self) :
        self.assertIsNotNone(self.p)

    def testEveryElementIsVisited(self) :
        self.p.filename = "../../test-data/meco-energy-test-data.xml"
        expectedCount = 656
        self.p.parseXML(True)
        print "element count = %s" % self.p.elementCount
        self.assertEqual(self.p.elementCount, expectedCount)

    def testAllTableNamesArePresent(self) :
        self.p.filename = "../../test-data/meco-energy-test-data.xml"
        self.p.parseXML(True)
        fail = 0

        for key in self.p.tableNameCount.keys():
            print key + ": ",
            print self.p.tableNameCount[key]

        for c in self.p.tableNameCount.values() :
            if c < 1 :
                fail = 1
        self.assertEqual(fail, 0)

if __name__ == '__main__' :
    unittest.main()
