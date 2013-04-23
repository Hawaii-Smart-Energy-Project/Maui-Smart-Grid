#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'

import unittest
from mecoconfig import MECOConfiger


class TestMECOConfig(unittest.TestCase):
    def setUp(self):
        self.configer = MECOConfiger()

    def test_init(self):
        localConfiger = MECOConfiger()
        self.assertIsInstance(self.configer, type(localConfiger))

if __name__ == '__main__':
    unittest.main()
