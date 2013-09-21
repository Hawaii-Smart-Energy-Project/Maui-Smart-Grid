#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'
__copyright__ = 'Copyright (c) 2013, University of Hawaii Smart Energy Project'
__license__ = 'https://raw.github' \
              '.com/Hawaii-Smart-Energy-Project/Maui-Smart-Grid/master/BSD' \
              '-LICENSE.txt'

import unittest
from meco_fk import MECOFKDeterminer


class TestMECOFKeys(unittest.TestCase):
    """
    Unit tests for MECO DB foreign keys.
    """

    def setUp(self):
        self.fkeys = MECOFKDeterminer()

    def test_init(self):
        self.assertIsInstance(self.fkeys, MECOFKDeterminer)

    # @todo write foreign key tests\
    def test_foreign_keys(self):
        pass

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
