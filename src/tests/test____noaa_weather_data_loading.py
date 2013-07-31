#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'

import unittest


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)


    def testLoadDataSinceLastLoaded(self):
        """
        Data should be loaded since the last data present in the database.
        """
        pass


    def testGetLastLoadedDate(self):
        pass


if __name__ == '__main__':
    unittest.main()
