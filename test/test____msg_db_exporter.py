#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'

import unittest
from msg_logger import MSGLogger
from msg_db_exporter import MSGDBExporter
import hashlib
import os
import httplib2
from apiclient import http
import datetime


class MSGDBExporterTester(unittest.TestCase):
    def setUp(self):
        self.logger = MSGLogger(__name__, 'DEBUG')
        self.exporter = MSGDBExporter()


    def testListRemoteFiles(self):
        self.logger.log('Testing listing of remote files.', 'INFO')
        title = ''
        id = ''
        for item in self.exporter.cloudFiles['items']:
            title = item['title']
            # print title
            id = item['id']
            # print "id = %s" % id
            self.assertIsNot(title, '')
            self.assertIsNot(id, '')


    def testGetMD5Sum(self):
        self.logger.log('Testing getting the MD5 sum.', 'info')
        md5sum = ''
        for item in self.exporter.cloudFiles['items']:
            # print item['title']
            md5sum = item['md5Checksum']
            # print md5sum
        self.assertEquals(len(md5sum), 32)



    def testGetFileIDsForFilename(self):
        """
        Retrieve the matching file IDs for the given file name.
        """

        # @todo Upload file for testing.
        self.logger.log("Uploading test data.")

        filePath = "../test-data/db-export/meco_v3.sql.gz"

        uploadResult = self.exporter.uploadDBToCloudStorage(filePath)

        self.assertTrue(uploadResult)

        self.logger.log('Testing getting the file ID for a filename.')

        fileIDs = self.exporter.fileIDForFileName('meco_v3.sql.gz')
        self.logger.log("file ids = %s" % fileIDs, 'info')

        self.assertIsNotNone(fileIDs)


    def testUploadTestData(self):
        """
        Upload a test data file for unit testing of DB export.
        """

        return

        self.logger.log("Uploading test data.")

        filePath = "../test-data/db-export/meco_v3.sql.gz"
        print hashlib.md5(filePath).hexdigest()

        uploadResult = self.exporter.uploadDBToCloudStorage(filePath)

        for item in self.exporter.cloudFiles['items']:
            print 'item: %s' % item['title']
            print 'md5: %s' % item['md5Checksum']

        self.assertTrue(uploadResult)

    def testDeleteOutdatedFiles(self):
        # @todo Prevent deleting files uploaded today.
        # @todo Prevent deleting NON-testing files.

        return

        self.logger.log("Test deleting outdated files.")

        self.logger.log("Uploading test data.")

        filePath = "../test-data/db-export/meco_v3.sql.gz"

        uploadResult = self.exporter.uploadDBToCloudStorage(filePath)

        cnt = self.exporter.deleteOutdatedFiles(
            minAge = datetime.timedelta(days = -2),
            maxAge = datetime.timedelta(days = 0))
        self.assertGreater(cnt, 0)


    def tearDown(self):
        """
        Delete all test items.
        """

        pass


if __name__ == '__main__':
    unittest.main()

    # Run a single test:
    #mySuite = unittest.TestSuite()
    #mySuite.addTest(MSGDBExporterTester('testGetMD5Sum'))
    #unittest.TextTestRunner().run(mySuite)
