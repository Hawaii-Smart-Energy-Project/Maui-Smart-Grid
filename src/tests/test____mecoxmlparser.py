#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'

import unittest
from mecoxmlparser import MECOXMLParser

"""@todo: this test needs static test data.
"""

class TestMECOXMLParser(unittest.TestCase) :
    """Unit tests for MECO XML Parser.
    """

    def setUp(self) :
        self.p = MECOXMLParser()

    def testMECOXMLParserCanBeInited(self) :
        self.assertIsNotNone(self.p)

    def testEveryElementIsVisited(self) :
        expectedCount = 100000;
        self.p.parseXML()
        self.assertEqual(self.p.elementCount, expectedCount)

    def testAllTableNamesArePresent(self) :
        self.p.parseXML()
        fail = 0
        for c in self.p.tableNameCount.values() :
            if c < 1 :
                fail = 1
        self.assertEqual(fail, 0)

if __name__ == '__main__' :
    unittest.main()
