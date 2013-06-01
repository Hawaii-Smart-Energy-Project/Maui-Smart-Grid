#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'

import unittest
from mecodbconnect import MECODBConnector
import mecodbconnect

class TestMECODBConnect(unittest.TestCase):
    """These tests require a database connection be available.
    """

    def setUp(self):
        self.connector = MECODBConnector(True)
        self.conn = self.connector.connectDB()

    def test_init(self):
        self.assertTrue(
            isinstance(self.connector, mecodbconnect.MECODBConnector),
            "self.connection is an instance of MECODBConnector")

    def test_db_connection(self):
        """
        DB can be connected to.
        """
        self.assertIsNotNone(self.conn)

    def tearDown(self):
        self.connector.closeDB(self.conn)

if __name__ == '__main__':
    unittest.main()
