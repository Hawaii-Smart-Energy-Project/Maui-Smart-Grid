#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'

import unittest
from meco_fk import MECOFKDeterminer


class TestMECOFKeys(unittest.TestCase):
    """Unit tests for MECO DB foreign keys.
    """

    def setUp(self):
        self.fkeys = MECOFKDeterminer()

    def test_init(self):
        self.assertIsInstance(self.fkeys, MECOFKDeterminer)

    # @todo write foreign key tests

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
