#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'
__copyright__ = 'Copyright (c) 2013, University of Hawaii Smart Energy Project'
__license__ = 'https://raw.github' \
              '.com/Hawaii-Smart-Energy-Project/Maui-Smart-Grid/master/BSD' \
              '-LICENSE.txt'

import unittest
from meco_plotting import MECOPlotting

class TestMECOPlotting(unittest.TestCase):

    def setUp(self):
        self.plotter = MECOPlotting()
        pass

    def tearDown(self):
        pass

    def testPlot(self):
        pass
