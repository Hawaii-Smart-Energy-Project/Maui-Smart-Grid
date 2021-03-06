#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'
__copyright__ = 'Copyright (c) 2014, University of Hawaii Smart Energy Project'
__license__ = 'https://raw.github' \
              '.com/Hawaii-Smart-Energy-Project/Maui-Smart-Grid/master/BSD' \
              '-LICENSE.txt'

import unittest
from sek.logger import SEKLogger
from msg_db_exporter import MSGDBExporter
from apiclient import http
import datetime
from apiclient import errors
from msg_configer import MSGConfiger
import os
import shutil
import gzip
from msg_file_util import MSGFileUtil
from msg_db_connector import MSGDBConnector
from msg_db_util import MSGDBUtil
import re
from msg_python_util import MSGPythonUtil
import itertools
import time
from msg_time_util import MSGTimeUtil
from msg_types import MSGNotificationHistoryTypes

EARLIEST_DATE = MSGTimeUtil().datetimeForString('2011-01-01 00:00')


class MSGDBExporterTester(unittest.TestCase):
    """
    Unit tests for the MSG Cloud Exporter.
    """


    def setUp(self):
        self.logger = SEKLogger(__name__, 'DEBUG')
        self.configer = MSGConfiger()
        self.exporter = MSGDBExporter()
        self.testDir = 'db_exporter_test'
        self.uncompressedTestFilename = 'meco_v3_test_data.sql'
        self.compressedTestFilename = 'meco_v3_test_data.sql.gz'
        self.exportTestDataPath = self.configer.configOptionValue('Testing',
                                                                  'export_test_data_path')
        self.fileUtil = MSGFileUtil()
        self.fileChunks = []
        self.testDataFileID = ''
        self.pyUtil = MSGPythonUtil()
        self.timeUtil = MSGTimeUtil()

        conn = None
        try:
            conn = MSGDBConnector().connectDB()
        except Exception as detail:
            self.logger.log("Exception occurred: {}".format(detail), 'error')
            exit(-1)

        self.logger.log("conn = {}".format(conn), 'debug')
        self.assertIsNotNone(conn)

        # Create a temporary working directory.
        try:
            os.mkdir(self.testDir)
        except OSError as detail:
            self.logger.log(
                'Exception during creation of temp directory: %s' % detail,
                'ERROR')


    def tearDown(self):
        """
        Delete all test items.
        """

        REMOVE_TEMPORARY_FILES = True
        if REMOVE_TEMPORARY_FILES:
            try:
                self.logger.log("Removing local test files {}, {}.".format(
                    self.uncompressedTestFilename, self.compressedTestFilename),
                                'debug')
                os.remove(os.path.join(os.getcwd(), self.testDir,
                                       self.uncompressedTestFilename))
                os.remove(os.path.join(os.getcwd(), self.testDir,
                                       self.compressedTestFilename))
            except OSError as detail:
                self.logger.log(
                    'Exception while removing temporary files: {}'.format(
                        detail), 'SILENT')
            try:
                os.remove(os.path.join(os.getcwd(), self.testDir,
                                       self.compressedTestFilename))
            except OSError as detail:
                self.logger.log(
                    'Exception while removing temporary files: {}'.format(
                        detail), 'SILENT')
            try:
                for f in self.fileChunks:
                    os.remove(f)
            except OSError as detail:
                self.logger.log(
                    'Exception while removing temporary files: {}'.format(
                        detail), 'DEBUG')

        try:
            os.rmdir(self.testDir)
        except OSError as detail:
            self.logger.log(
                'Exception while removing directory: {}'.format(detail),
                'ERROR')

        # Keep deleting from the cloud until there are no more to delete.
        def deleteFromCloud():
            self.logger.log("deleting from cloud", 'debug')
            try:
                fileIDToDelete = self.exporter.fileIDForFileName(
                    self.compressedTestFilename)
                if fileIDToDelete is None:
                    return
                self.logger.log("file ID to delete: {}".format(fileIDToDelete),
                                'DEBUG')
                self.exporter.driveService.files().delete(
                    fileId = '{}'.format(fileIDToDelete)).execute()
                deleteFromCloud()
            except (TypeError, http.HttpError) as e:
                self.logger.log('Delete not successful: {}'.format(e), 'DEBUG')


        deleteFromCloud()


    def _upload_test_data_to_cloud(self):
        """
        Provide an upload of test data that can be used in other tests.

        Side effect: Store the file ID as an ivar.
        """
        self.logger.log("Uploading test data for caller: {}".format(
            self.pyUtil.callerName()))

        filePath = "{}/{}".format(self.exportTestDataPath,
                                  self.compressedTestFilename)
        self.logger.log('Uploaded {}.'.format(filePath), 'info')

        uploadResult = self.exporter.uploadFileToCloudStorage(filePath)
        self.logger.log('upload result: {}'.format(uploadResult))

        self.testDataFileID = self.exporter.fileIDForFileName(
            self.compressedTestFilename)
        self.logger.log("Test file ID is {}.".format(self.testDataFileID))


    def test_markdown_list_of_downloadable_files(self):
        """
        Match the Markdown line entry for the uploaded file.
        """
        # @REVIEWED
        self._upload_test_data_to_cloud()
        self.assertEquals(len(filter(lambda x: self.testDataFileID in x,
                                     self.exporter.markdownListOfDownloadableFiles().splitlines())),
                          1)


    def test_get_md5_sum_from_cloud(self):
        """
        Test retrieving the MD5 sum from the cloud.
        """
        # @REVIEWED
        self.logger.log('Testing getting the MD5 sum.', 'info')
        self._upload_test_data_to_cloud()
        testFileMD5 = filter(lambda x: x['id'] == self.testDataFileID,
                             self.exporter.cloudFiles['items'])[0][
            'md5Checksum']
        self.assertEquals(len(testFileMD5), 32)
        self.assertTrue(re.match(r'[0-9A-Za-z]+', testFileMD5))


    def test_get_file_id_for_nonexistent_file(self):
        """
        Test getting a file ID for a nonexistent file.
        """
        # @REVIEWED
        fileIDs = self.exporter.fileIDForFileName('nonexistent_file')
        self.logger.log("file ids = {}".format(fileIDs), 'info')
        self.assertIsNone(fileIDs)


    def test_upload_test_data(self):
        """
        Upload a test data file for unit testing of DB export.

        The unit test data file is a predefined set of test data stored in
        the test data path of the software distribution.
        """
        # @REVIEWED

        self._upload_test_data_to_cloud()
        self.assertGreater(len(self.testDataFileID), 0)
        self.assertTrue(re.match(r'[0-9A-Za-z]+', self.testDataFileID))


    def test_adding_reader_permissions(self):
        """
        Add reader permissions to a file that was uploaded.
        """
        # @REVIEWED
        self.logger.log("Testing adding reader permissions.")
        self._upload_test_data_to_cloud()

        email = self.configer.configOptionValue('Testing',
                                                'tester_email_address')
        service = self.exporter.driveService
        try:
            id_resp = service.permissions().getIdForEmail(
                email = email).execute()
            print id_resp

        except errors.HttpError as detail:
            print 'Exception while getting ID for email: {}'.format(detail)

        new_permission = {'value': email, 'type': 'user', 'role': 'reader'}
        try:
            self.logger.log('Adding reader permission', 'INFO')
            fileIDToAddTo = self.testDataFileID

            # The permission dict is being output to stdout here.
            resp = service.permissions().insert(fileId = fileIDToAddTo,
                                                sendNotificationEmails = False,
                                                body = new_permission).execute()
        except errors.HttpError as detail:
            self.logger.log(
                'Exception while adding reader permissions: {}'.format(detail),
                'error')


        def permission_id(email):
            try:
                id_resp = service.permissions().getIdForEmail(
                    email = email).execute()
                return id_resp['id']
            except errors.HttpError as error:
                self.logger.log("HTTP error: {}".format(error))


        permission = {}
        try:
            permission = service.permissions().get(fileId = self.testDataFileID,
                                                   permissionId = permission_id(
                                                       email)).execute()
        except errors.HttpError as error:
            self.logger.log("HTTP error: {}".format(error))

        self.assertEquals(permission['role'], 'reader')


    def test_create_compressed_archived(self):
        """
        * Copy test data to a temp directory (self.testDir).
        * Create a checksum for test data.
        * Create a gzip-compressed archive.
        * Extract gzip-compressed archive.
        * Create a checksum for the uncompressed data.
        * Compare the checksums.
        """
        # @REVIEWED

        self.logger.log('Testing verification of a compressed archive.')

        self.logger.log('cwd {}'.format(os.getcwd()))
        fullPath = '{}'.format(os.path.join(os.getcwd(), self.testDir,
                                            self.uncompressedTestFilename))
        shutil.copyfile('{}/{}'.format(self.exportTestDataPath,
                                       self.uncompressedTestFilename), fullPath)

        md5sum1 = self.fileUtil.md5Checksum(fullPath)

        self.exporter.fileUtil.gzipCompressFile(fullPath)

        try:
            os.remove(os.path.join(os.getcwd(), self.testDir,
                                   self.uncompressedTestFilename))
        except OSError as detail:
            self.logger.log('Exception while removing: {}'.format(detail),
                            'ERROR')

        # Extract archived data and generate checksum.
        src = gzip.open('{}{}'.format(fullPath, '.gz'), "rb")
        uncompressed = open(fullPath, "wb")
        decoded = src.read()
        uncompressed.write(decoded)
        uncompressed.close()

        md5sum2 = self.fileUtil.md5Checksum(fullPath)

        self.assertEqual(md5sum1, md5sum2,
                         'Checksums are not equal for original and new '
                         'decompressed archive.')


    def test_export_db(self):
        """
        Perform a quick test of the DB export method using Testing Mode.

        This requires sudo authorization to complete.
        """
        # @REVIEWED

        self.logger.log('Testing exportDB using the testing DB.')

        # @todo handle case where testing db does not exist.

        dbs = ['test_meco']
        ids = self.exporter.exportDBs(databases = dbs, toCloud = True,
                                      localExport = True)
        self.logger.log('Count of exports: {}'.format(len(ids)))
        self.assertEquals(len(ids), 1, "Count of exported files is wrong.")

        map(self.exporter.deleteFile, ids)


    def test_split_archive(self):
        """
        Test splitting an archive into chunks.
        """
        # @REVIEWED
        self.logger.log('Testing archive splitting.')
        fullPath = '{}/{}'.format(self.exportTestDataPath,
                                  self.compressedTestFilename)
        self.logger.log('fullpath: {}'.format(fullPath))
        shutil.copyfile(fullPath, '{}/{}'.format(self.testDir,
                                                 self.compressedTestFilename))
        fullPath = '{}/{}'.format(self.testDir, self.compressedTestFilename)

        self.fileChunks = self.fileUtil.splitLargeFile(fullPath = fullPath,
                                                       numChunks = 3)
        self.assertEquals(len(self.fileChunks), 3)


    def test_get_file_size(self):
        """
        Test retrieving local file sizes.
        """
        # @REVIEWED
        fullPath = '{}/{}'.format(self.exportTestDataPath,
                                  self.compressedTestFilename)
        fSize = self.fileUtil.fileSize(fullPath)
        self.logger.log('size: {}'.format(fSize))
        self.assertEqual(fSize, 12279, 'File size is correct.')


    def test_upload_export_files_list(self):
        """
        TBW
        """
        pass


    def test_checksum_after_upload(self):
        """
        TBW
        """
        pass


    def test_dump_exclusions_dictionary(self):
        """
        Verify the exclusions dictionary by its type.
        :return:
        """
        # @REVIEWED
        exclusions = self.exporter.dumpExclusionsDictionary()

        if exclusions:
            self.assertEquals(type({}), type(exclusions))


    def test_move_to_final(self):
        """
        Test moving a file to the final destination path.
        """
        # @REVIEWED
        self.logger.log('Testing moving to final path {}.'.format(
            self.configer.configOptionValue('Export', 'db_export_final_path')))

        origCompressedFile = '{}/{}'.format(
            self.configer.configOptionValue('Export', 'export_test_data_path'),
            self.compressedTestFilename)
        newCompressedFile = '{}/{}'.format(
            self.configer.configOptionValue('Export', 'export_test_data_path'),
            'temp_test_file')

        shutil.copyfile(origCompressedFile, newCompressedFile)

        self.exporter.moveToFinalPath(compressedFullPath = newCompressedFile)

        self.assertTrue(os.path.isfile('{}/{}'.format(
            self.configer.configOptionValue('Export', 'db_export_final_path'),
            'temp_test_file')))

        # Remove the test file.
        os.remove('{}/{}'.format(
            self.configer.configOptionValue('Export', 'db_export_final_path'),
            'temp_test_file'))


    def test_log_successful_export(self):
        """
        Test logging of export results to the export history table.
        """
        # @REVIEWED
        self.assertTrue(self.exporter.logSuccessfulExport(name = 'test_export',
                                                          url =
                                                          'http://test_url',
                                                          datetime = 0,
                                                          size = 100))

        conn = MSGDBConnector().connectDB()
        cursor = conn.cursor()
        dbUtil = MSGDBUtil()

        self.assertTrue(
            dbUtil.executeSQL(cursor, 'select * from "ExportHistory" where '
                                      'timestamp = '
                                      'to_timestamp(0)'))

        self.assertEqual(len(cursor.fetchall()), 1,
                         "There should only be one result row.")

        self.assertTrue(
            dbUtil.executeSQL(cursor, 'delete from "ExportHistory" where '
                                      'timestamp = to_timestamp(0)'))
        conn.commit()


    def test_metadata_of_file_id(self):
        """
        Test getting the metadata for a file ID.
        """
        # @REVIEWED
        self._upload_test_data_to_cloud()

        self.logger.log('metadata: {}'.format(
            self.exporter.metadataOfFileID(self.testDataFileID)))

        self.assertTrue(re.match(r'[0-9A-Za-z]+', self.testDataFileID))


    def test_filename_for_file_id(self):
        """
        Test returning a file name given a file ID.
        """
        # @REVIEWED
        self._upload_test_data_to_cloud()
        self.assertEquals(
            self.exporter.filenameForFileID(fileID = self.testDataFileID),
            self.compressedTestFilename)


    def test_outdated_files(self):
        # @REVIEWED
        self._upload_test_data_to_cloud()
        time.sleep(1)
        self.logger.log("outdated:")

        # For debugging:
        for item in self.exporter.outdatedFiles(
                daysBeforeOutdated = datetime.timedelta(
                        days = -1)): self.logger.log(
            "name: {}, created date: {}".format(item['originalFilename'],
                                                item['createdDate']), 'debug')

        # Get all the outdated files where outdated is equal to anything
        # uploaded today or later.
        self.assertTrue(self.exporter.outdatedFiles(
            daysBeforeOutdated = datetime.timedelta(days = -1))[0][
                            'id'] == self.testDataFileID)

        self.logger.log('-----')


    def test_delete_outdated(self):
        """
        TBW
        """
        pass


    def test_list_of_downloadable_files(self):
        """
        Test the list of downloadable files used by the available files page.
        """
        # @REVIEWED
        self._upload_test_data_to_cloud()
        self.assertEquals(len(
            filter(lambda row: row['id'] == self.testDataFileID,
                   self.exporter.listOfDownloadableFiles())), 1,
                          "Test file not present.")


    def test_count_of_db_exports(self):
        count = self.exporter.countOfDBExports(EARLIEST_DATE)
        self.logger.log(count,'DEBUG')
        self.assertTrue(int(count) or int(count) == int(0))


    def test_count_of_cloud_files(self):
        count = self.exporter.countOfCloudFiles()
        self.assertTrue(int(count) or int(count) == int(0))


    def test_plaintext_list_of_downloadable_files(self):
        """
        This test handles content both with content links and without content
        links.
        """
        content = self.exporter.plaintextListOfDownloadableFiles()
        self.assertRegexpMatches(content,
                                 '\d+-\d+-\d+.*\,'
                                 '\s+\d+-\d+-\d+T\d+:\d+:\d+\.\d+Z\,\s+\d+\sB')


    def test_last_report_date(self):
        last_report = self.exporter.notifier.lastReportDate(
            types = MSGNotificationHistoryTypes,
            noticeType = MSGNotificationHistoryTypes.MSG_EXPORT_SUMMARY)
        self.assertTrue(last_report is None or last_report > EARLIEST_DATE)

    def test_current_export_summary(self):
        self.assertRegexpMatches(self.exporter.currentExportSummary(),
                                 re.compile(
                                     'last.*databases.*free.*currently.*accessed.*',
                                     flags = re.IGNORECASE | re.DOTALL))


    # def test_send_current_export_summary(self):
    #     self.exporter.notifier.sendNotificationEmail(
    #         self.exporter.currentExportSummary(), testing = True)


if __name__ == '__main__':
    RUN_SELECTED_TESTS = True

    if RUN_SELECTED_TESTS:

        sudo_tests = ['test_export_db']

        nonsudo_tests = ['test_upload_test_data', 'test_log_successful_export',
                         'test_metadata_of_file_id',
                         'test_dump_exclusions_dictionary',
                         'test_filename_for_file_id', 'test_move_to_final',
                         'test_get_md5_sum_from_cloud', 'test_split_archive',
                         'test_get_file_size',
                         'test_get_file_id_for_nonexistent_file',
                         'test_create_compressed_archived',
                         'test_adding_reader_permissions',
                         'test_markdown_list_of_downloadable_files',
                         'test_outdated_files', 'test_count_of_db_exports',
                         'test_count_of_cloud_files',
                         'test_plaintext_list_of_downloadable_files',
                         'test_last_report_date', 'test_current_export_summary']

        selected_tests = [x for x in itertools.chain(sudo_tests, nonsudo_tests)]

        # For testing:
        # selected_tests = ['test_count_of_db_exports']

        mySuite = unittest.TestSuite()
        for t in selected_tests:
            mySuite.addTest(MSGDBExporterTester(t))
        unittest.TextTestRunner().run(mySuite)
    else:
        unittest.main()
