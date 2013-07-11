#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'

import unittest
from meco_db_connector import MSGDBConnector
import meco_db_connector

class TestMECODBConnect(unittest.TestCase):
    """These tests require a database connection be available.
    """

    def setUp(self):
        self.connector = MSGDBConnector(True)
        self.conn = self.connector.connectDB()

    def test_init(self):
        self.assertTrue(
            isinstance(self.connector, meco_db_connector.MSGDBConnector),
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
