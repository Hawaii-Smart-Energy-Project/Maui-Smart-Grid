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
import shutil
import gzip
from msg_file_util import MSGFileUtil


class MSGDBExporterTester(unittest.TestCase):
    """
    Unit tests for the MSG Cloud Exporter.
    """

    def setUp(self):
        self.logger = MSGLogger(__name__, 'DEBUG')
        self.configer = MSGConfiger()
        self.exporter = MSGDBExporter()
        self.testDir = 'db_exporter_test'
        self.uncompressedTestFilename = 'meco_v3_test_data.sql'
        self.compressedTestFilename = 'meco_v3_test_data.sql.gz'
        self.exportTestDataPath = self.configer.configOptionValue('Testing',
                                                                  'export_test_data_path')
        self.fileUtil = MSGFileUtil()
        self.fileChunks = []

        # Create a temporary working directory.
        try:
            os.mkdir(self.testDir)
        except OSError as detail:
            self.logger.log(
                'Exception during creation of temp directory: %s' % detail,
                'ERROR')

    def testListRemoteFiles(self):
        self.logger.log('Testing listing of remote files.', 'INFO')
        title = ''
        id = ''
        for item in self.exporter.cloudFiles['items']:
            title = item['title']
            id = item['id']
            self.assertIsNot(title, '')
            self.assertIsNot(id, '')

    def testGetMD5SumFromCloud(self):
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

        filePath = "%s/%s" % (
            self.exportTestDataPath, self.compressedTestFilename)

        uploadResult = self.exporter.uploadDBToCloudStorage(filePath)

        self.assertTrue(uploadResult)

        self.logger.log('Testing getting the file ID for a filename.')

        fileIDs = self.exporter.fileIDForFileName(self.compressedTestFilename)
        self.logger.log("file ids = %s" % fileIDs, 'info')

        self.assertIsNotNone(fileIDs)


    def testUploadTestData(self):
        """
        Upload a test data file for unit testing of DB export.
        """

        self.logger.log("Uploading test data.")

        filePath = "%s/%s" % (
            self.exportTestDataPath, self.compressedTestFilename)
        self.logger.log('Uploaded %s.' % filePath, 'info')

        uploadResult = self.exporter.uploadDBToCloudStorage(filePath)

        self.assertTrue(uploadResult)


    def testDeleteOutdatedFiles(self):
        """
        The timestamp of an uploaded file should be set in the past to provide
        the ability to test the deleting of outdated files.
        """

        # @todo Prevent deleting files uploaded today.
        # @todo Prevent deleting NON-testing files.

        self.logger.log("Test deleting outdated files.")

        self.logger.log("Uploading test data.")

        filePath = "%s/%s" % (
            self.exportTestDataPath, self.compressedTestFilename)

        uploadResult = self.exporter.uploadDBToCloudStorage(filePath)

        cnt = self.exporter.deleteOutdatedFiles(
            minAge = datetime.timedelta(days = -2),
            maxAge = datetime.timedelta(days = 0))
        self.assertGreater(cnt, 0)


    def testAddingReaderPermissions(self):
        """
        Add reader permissions to a file that was uploaded.

        @todo Needs update after cloud export restoration.
        """

        self.logger.log("Testing adding reader permissions.")
        self.logger.log("Uploading test data.")
        filePath = "%s/%s" % (
            self.exportTestDataPath, self.compressedTestFilename)
        uploadResult = self.exporter.uploadDBToCloudStorage(filePath)
        email = self.configer.configOptionValue('Testing', 'tester_email')
        service = self.exporter.driveService
        try:
            id_resp = service.permissions().getIdForEmail(
                email = email).execute()
            print id_resp

        except errors.HttpError as detail:
            print 'Exception while getting ID for email: %s' % detail

        new_permission = {'value': email, 'type': 'user', 'role': 'reader'}
        try:
            self.logger.log('Adding reader permission', 'INFO')
            fileIDToAddTo = self.exporter.fileIDForFileName(
                self.compressedTestFilename)

            # The permission dict is being output to stdout here.
            resp = service.permissions().insert(fileId = fileIDToAddTo,
                                                body = new_permission).execute()
        except errors.HttpError as detail:
            self.logger.log(
                'Exception while adding reader permissions: %s' % detail,
                'error')


    def testCreateCompressedArchived(self):
        """
        * Copy test data to a temp directory.
        * Create a checksum for test data.
        * Create a gzip-compressed archive.
        * Extract gzip-compressed archive.
        * Create a checksum for the uncompressed data.
        * Compare the checksums.

        @todo Needs update after cloud export restoration.
        """

        self.logger.log('Testing verification of a compressed archive.')

        self.logger.log('cwd %s' % os.getcwd())
        fullPath = '%s' % (
            os.path.join(os.getcwd(), self.testDir,
                         self.uncompressedTestFilename))
        shutil.copyfile(
            '%s/%s' % (self.exportTestDataPath, self.uncompressedTestFilename),
            fullPath)

        md5sum1 = self.fileUtil.md5Checksum(fullPath)

        self.exporter.fileUtil.gzipCompressFile(fullPath)

        try:
            os.remove(os.path.join(os.getcwd(), self.testDir,
                                   self.uncompressedTestFilename))
        except OSError as detail:
            self.logger.log('Exception while removing: %s' % detail, 'ERROR')

        # Extract archived data and generate checksum.
        src = gzip.open('%s%s' % (fullPath, '.gz'), "rb")
        uncompressed = open(fullPath, "wb")
        decoded = src.read()
        uncompressed.write(decoded)
        uncompressed.close()

        md5sum2 = self.fileUtil.md5Checksum(fullPath)

        self.assertEqual(md5sum1, md5sum2,
                         'Checksums are equal for original and new '
                         'decompressed archive.')

    def testExportDB(self):
        """
        Perform a quick test of the DB export method using Testing Mode.
        """

        self.logger.log('Testing exportDB')
        dbs = ['test_meco']
        success = self.exporter.exportDB(databases = dbs, toCloud = True,
                                         localExport = True, chunkSize = 14000)
        self.logger.log('Success: %s' % success)
        self.assertTrue(success, "Export was successful.")


    def testSplitArchive(self):
        """
        Test splitting an archive into chunks.
        """

        fullPath = '%s/%s' % (
            self.exportTestDataPath, self.compressedTestFilename)
        self.logger.log('fullpath: %s' % fullPath)
        shutil.copyfile(fullPath, '%s/%s' % (
            self.testDir, self.compressedTestFilename))
        fullPath = '%s/%s' % (
            self.testDir, self.compressedTestFilename)

        self.fileChunks = self.fileUtil.splitFile(fullPath = fullPath,
                                                  chunkSize = 6000)

        self.assertGreater(len(self.fileChunks), 0,
                           'Chunk number is greater than zero.')


    def tearDown(self):
        """
        Delete all test items.

        @todo Needs re-evaluation after cloud export restoration.
        """

        REMOVE_TEMPORARY_FILES = True
        if REMOVE_TEMPORARY_FILES:
            try:
                os.remove(os.path.join(os.getcwd(), self.testDir,
                                       self.uncompressedTestFilename))
                os.remove(os.path.join(os.getcwd(), self.testDir,
                                       self.compressedTestFilename))
            except OSError as detail:
                self.logger.log(
                    'Exception while removing temporary files: %s' % detail,
                    'SILENT')
            try:
                os.remove(os.path.join(os.getcwd(), self.testDir,
                                       self.compressedTestFilename))
            except OSError as detail:
                self.logger.log(
                    'Exception while removing temporary files: %s' % detail,
                    'SILENT')
            try:
                for f in self.fileChunks:
                    os.remove(f)
            except OSError as detail:
                self.logger.log(
                    'Exception while removing temporary files: %s' % detail,
                    'DEBUG')

        try:
            # Might need recursive delete here to handle unexpected cases.
            os.rmdir(self.testDir)
        except OSError as detail:
            self.logger.log('Exception while removing directory: %s' % detail,
                            'ERROR')

        deleteSuccessful = True

        # Keep deleting from the cloud until there is no more to delete.
        while deleteSuccessful:
            try:
                fileIDToDelete = self.exporter.fileIDForFileName(
                    self.compressedTestFilename)
                self.logger.log("file ID to delete: %s" % fileIDToDelete,
                                'DEBUG')
                self.exporter.driveService.files().delete(
                    fileId = '%s' % fileIDToDelete).execute()
            except (TypeError, http.HttpError) as e:
                self.logger.log('Delete not successful: %s' % e, 'SILENT')
                break


if __name__ == '__main__':
    RUN_SELECTED_TESTS = True

    if RUN_SELECTED_TESTS:
        selected_tests = ['testSplitArchive', 'testExportDB']
        mySuite = unittest.TestSuite()
        for t in selected_tests:
            mySuite.addTest(MSGDBExporterTester(t))
        unittest.TextTestRunner().run(mySuite)
    else:
        unittest.main()
