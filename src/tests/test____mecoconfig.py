#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'

import unittest
from mecoconfig import MECOConfiger


class TestMECOConfig(unittest.TestCase):
    def setUp(self):
        self.configer = MECOConfiger()

    def test_init(self):
        # @todo Improve this test by using direct introspection instead of this roundabout method.
        localConfiger = MECOConfiger()
        self.assertIsInstance(self.configer, type(localConfiger))

    def test_get_debugging(self):
        """
        Verify the debugging option in the configuration file.
        """

        debugging = self.configer.configOptionValue("Debugging","debug")

        if debugging is False:
            self.assertFalse(debugging, "Debugging/debug is not set to False.")
        elif debugging is True:
            self.assertTrue(debugging, "Debugging/debug is not set to True.")
        else:
            self.assertTrue(False, "Debugging/debug does not have a valid value.")


if __name__ == '__main__':
    unittest.main()
