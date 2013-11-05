#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'

import unittest
from msg_logger import MSGLogger
from msg_db_exporter import MSGDBExporter


class MSGDBExporterTester(unittest.TestCase):
    def setUp(self):
        self.logger = MSGLogger(__name__)
        self.exporter = MSGDBExporter()

    def testListRemoteFiles(self):
        title=''
        id=''
        for item in self.exporter.cloudFiles['items']:
            title=item['title']
            print title
            id = item['id']
            print id
        self.assertIsNot(title, '')
        self.assertIsNot(id, '')

    def testGetMD5Sum(self):
        md5sum = ''
        for item in self.exporter.cloudFiles['items']:
            print item['title']
            md5sum = item['md5Checksum']
            print md5sum
        self.assertEquals(len(md5sum),32)

if __name__ == '__main__':
    unittest.main()
    #mySuite = unittest.TestSuite()
    #mySuite.addTest(MSGDBExporterTester('testGetMD5Sum'))
    #unittest.TextTestRunner().run(mySuite)
