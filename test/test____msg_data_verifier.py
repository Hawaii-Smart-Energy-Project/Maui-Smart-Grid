#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'
__copyright__ = 'Copyright (c) 2014, University of Hawaii Smart Energy Project'
__license__ = 'https://raw.github' \
              '.com/Hawaii-Smart-Energy-Project/Maui-Smart-Grid/master/BSD' \
              '-LICENSE.txt'

import unittest
from msg_data_verifier import MSGDataVerifier

class MSGDataVerifierTester(unittest.TestCase):

    def setUp(self):
        self.verifier = MSGDataVerifier()

    def testMECOReadingDupeCounts(self):
        print "total dupes = %d" % self.verifier.mecoReadingsDupeCount()

if __name__ == '__main__':
    unittest.main()
