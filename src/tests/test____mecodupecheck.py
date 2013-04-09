#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'

import unittest
from mecodupecheck import MECODupeChecker


class TestMECODupeChecker(unittest.TestCase):
    """Unit tests for duplicate checking.
    """

    def setUp(self):
        self.p = MECOXMLParser()
        self.dupeChecker = MECODupeChecker()

        # @todo insert test data to test db

    def findIndividualDupe(self):
        """Find a duplicate record when only one exists.
        """

        # @todo write test
        self.assertTrue(self.dupeChecker.meterIDAndEndTimeExists('100000',
                                                                 '2012-08-08 '
                                                                 '14:00'),
                        "Record should already exist")

    def testLoadOnTop(self):
        """If the same data set is loaded in succession, all values will be duplicated.
        Verify that this is true.
        """

        # @todo write test
