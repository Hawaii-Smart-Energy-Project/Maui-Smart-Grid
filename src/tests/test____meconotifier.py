#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'

import unittest
from meconotifier import MECONotifier

class TestMECONotifier(unittest.TestCase):
    """
    Unit tests for the MECO Notifier.
    """

    def setUp(self):
        self.notifier = MECONotifier()

    def tearDown(self):
        pass

    def testInit(self):
        self.assertIsNotNone(self.notifier, "Notifier has been initialized.")

if __name__ == '__main__':
    unittest.main()
