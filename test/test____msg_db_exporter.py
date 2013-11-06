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


class MSGDBExporterTester(unittest.TestCase):
    def setUp(self):
        self.logger = MSGLogger(__name__)
        self.exporter = MSGDBExporter()

    def testListRemoteFiles(self):
        title = ''
        id = ''
        for item in self.exporter.cloudFiles['items']:
            title = item['title']
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
        self.assertEquals(len(md5sum), 32)

    # @todo Upload file for testing.
    def testGetFileIDForFilename(self):
        fileID = self.exporter.fileIDForFileName(
            '2013-11-01_021138_meco_v3.sql.gz')
        print "file id = %s" % fileID
        self.assertIsNotNone(fileID)

    def testUploadTestData(self):
        """
        Upload a test data file for unit testing of DB export.
        """

        self.logger.log("Uploading test data.")

        filePath = "../test-data/db-export/meco_v3.sql.gz"
        print hashlib.md5(filePath).hexdigest()

        #for i in range(3):
        uploadResult = self.exporter.uploadDBToCloudStorage(filePath)

        for item in self.exporter.cloudFiles['items']:
            print 'item: %s' % item['title']
            print 'md5: %s' % item['md5Checksum']

        deleteSuccessful = True

        # Keep deleting until there is no more to delete.
        while deleteSuccessful:
            try:
                fileIDToDelete = self.exporter.fileIDForFileName(
                    'meco_v3.sql.gz')
                self.logger.log("file ID to delete: %s" % fileIDToDelete,
                                'DEBUG')
                self.exporter.driveService.files().delete(
                    fileId = '%s' % fileIDToDelete).execute()
            except (TypeError, http.HttpError) as e:
                self.logger.log('Delete not successful: %s' % e, 'DEBUG')
                break

        self.assertTrue(uploadResult)


if __name__ == '__main__':
    unittest.main()
    #mySuite = unittest.TestSuite()
    #mySuite.addTest(MSGDBExporterTester('testGetMD5Sum'))
    #unittest.TextTestRunner().run(mySuite)
