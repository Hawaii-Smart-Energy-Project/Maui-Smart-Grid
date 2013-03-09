#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'

import unittest
from mecodbconnect import MECODBConnector
import mecodbconnect


class TestMECODBConnect(unittest.TestCase) :
    def setUp(self) :
        self.conn = None
        self.connector = MECODBConnector()

    def test_init(self) :
        self.assertTrue(
            isinstance(self.connector, mecodbconnect.MECODBConnector))

    def test_db_connection(self) :
        """DB can be connected to.
        """
        self.conn = self.connector.connectDB()
        self.assertIsNotNone(self.conn)

if __name__ == '__main__' :
    unittest.main()
