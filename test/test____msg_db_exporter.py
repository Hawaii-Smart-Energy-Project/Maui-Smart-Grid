#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'

import unittest
from msg_logger import MSGLogger
from msg_db_exporter import MSGDBExporter
from apiclient import http
import datetime
from apiclient import errors
from msg_configer import MSGConfiger
import os


class MSGDBExporterTester(unittest.TestCase):
    def setUp(self):
        self.logger = MSGLogger(__name__, 'DEBUG')
        self.configer = MSGConfiger()
        self.exporter = MSGDBExporter()
        self.testDir = 'db_exporter_test'

        # Create a temporary working directory.
        try:
            os.mkdir(self.testDir)
        except OSError as detail:
            self.logger.log('Exception: %s' % detail, 'ERROR')


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

        self.logger.log("Uploading test data.")

        filePath = "../test-data/db-export/meco_v3.sql.gz"
        # print hashlib.md5(filePath).hexdigest()

        uploadResult = self.exporter.uploadDBToCloudStorage(filePath)

        # for item in self.exporter.cloudFiles['items']:
        #     print 'item: %s' % item['title']
        #     print 'md5: %s' % item['md5Checksum']

        self.assertTrue(uploadResult)


    def testDeleteOutdatedFiles(self):
        """
        The timestamp of an uploaded file should be set in the past to provide
        the ability to test the deleting of outdated files.
        """

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


    def testAddingReaderPermissions(self):
        """
        Add reader permissions to a file that was uploaded.
        """

        self.logger.log("Testing adding reader permissions.")
        self.logger.log("Uploading test data.")
        filePath = "../test-data/db-export/meco_v3.sql.gz"
        uploadResult = self.exporter.uploadDBToCloudStorage(filePath)
        email = self.configer.configOptionValue('Testing', 'tester_email')
        service = self.exporter.driveService
        try:
            id_resp = service.permissions().getIdForEmail(
                email = email).execute()
            print id_resp

        except errors.HttpError, error:
            print 'An error occured: %s' % error

        new_permission = {'value': email, 'type': 'user', 'role': 'reader'}
        try:
            self.logger.log('Adding reader permission', 'INFO')
            fileIDToAddTo = self.exporter.fileIDForFileName('meco_v3.sql.gz')

            # The permission dict is being output to stdout here.
            resp = service.permissions().insert(fileId = fileIDToAddTo,
                                                body = new_permission).execute()
        except errors.HttpError, error:
            print 'An error occurred: %s' % error


    def tearDown(self):
        """
        Delete all test items.
        """

        try:
            os.rmdir(self.testDir)
        except OSError as detail:
            self.logger.log('Exception: %s' % detail, 'ERROR')

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
                self.logger.log('Delete not successful: %s' % e, 'SILENT')
                break


if __name__ == '__main__':
    runSingleTest = False

    if runSingleTest:
        # Run a single test:
        mySuite = unittest.TestSuite()
        mySuite.addTest(MSGDBExporterTester('testAddingReaderPermissions'))
        unittest.TextTestRunner().run(mySuite)
    else:
        # Run all tests.
        unittest.main()

