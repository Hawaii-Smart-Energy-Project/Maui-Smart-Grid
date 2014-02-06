#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'
__copyright__ = 'Copyright (c) 2013, University of Hawaii Smart Energy Project'
__license__ = 'https://raw.github' \
              '.com/Hawaii-Smart-Energy-Project/Maui-Smart-Grid/master/BSD' \
              '-LICENSE.txt'

from msg_logger import MSGLogger
from msg_time_util import MSGTimeUtil
import subprocess
from msg_configer import MSGConfiger
import os
import httplib2
from apiclient.discovery import build
from apiclient.http import MediaFileUpload
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage
from apiclient import errors
import datetime
import hashlib
from functools import partial
from msg_file_util import MSGFileUtil
import time
from httplib import BadStatusLine


class MSGDBExporter(object):
    """
    Export MSG DBs as SQL scripts.

    Supports export to local storage and to cloud storage.
    """

    @property
    def cloudFiles(self):
        self._cloudFiles = self.driveService.files().list().execute()
        return self._cloudFiles

    @property
    def driveService(self):
        if self._driveService:
            return self._driveService

        if not self.credentialPath:
            raise Exception("Credential path is required.")
        storage = Storage('%s/google_api_credentials' % self.credentialPath)

        self.googleAPICredentials = storage.get()

        self.logger.log("Authorizing credentials.", 'info')
        http = httplib2.Http()
        http = self.googleAPICredentials.authorize(http)

        self.logger.log("Authorized.", 'info')

        self._driveService = build('drive', 'v2', http = http)
        return self._driveService


    def __init__(self):
        """
        Constructor.
        """

        self.logger = MSGLogger(__name__, 'DEBUG')
        self.timeUtil = MSGTimeUtil()
        self.configer = MSGConfiger()
        self.fileUtil = MSGFileUtil()

        # Google Drive parameters.
        self.clientID = self.configer.configOptionValue('Export',
                                                        'google_api_client_id')
        self.clientSecret = self.configer.configOptionValue('Export',
                                                            'google_api_client_secret')
        self.oauthScope = 'https://www.googleapis.com/auth/drive'
        self.oauthConsent = 'urn:ietf:wg:oauth:2.0:oob'
        self.googleAPICredentials = ''
        self.exportPath = self.configer.configOptionValue('Export',
                                                          'db_export_path')
        self.credentialPath = self.exportPath
        self.credentialStorage = Storage(
            '%s/google_api_credentials' % self.credentialPath)

        self._driveService = None
        self._cloudFiles = None
        self.filesToUpload = []


    def verifyExportChecksum(self, testing = False):
        """
        Verify the compressed export file using a checksum.

        * Save the checksum of the original uncompressed export data.
        * Extract the compressed file.
        * Verify the uncompressed export data.

        :param testing: When set to True, Testing Mode is used.
        """

        # Get the checksum of the original file.
        md5sum = self.fileUtil.md5Checksum(self.exportPath)
        self.logger.log('md5sum: %s' % md5sum)


    def exportDB(self, databases = None, toCloud = False, localExport = True,
                 testing = False, chunkSize = 0, numChunks = 0):
        """
        Export a set of DBs to local storage.

        This method makes use of

        pg_dump -s -h ${HOST} ${DB_NAME} > ${DUMP_TIMESTAMP}_{DB_NAME}.sql

        :param databases: List of database names that will be exported.
        :param toCloud: If set to True, then the export will also be copied to
        cloud storage.
        :param localExport: When set to True, the DB is exported locally.
        :param testing: Flag for testing mode. (@DEPRECATED)
        :param chunkSize: size in bytes of chunk size used for splitting.
        :returns: True if no errors have occurred, False otherwise.
        """

        noErrors = True

        host = self.configer.configOptionValue('Database', 'db_host')

        for db in databases:
            self.logger.log('Exporting %s using pg_dump.' % db, 'info')
            conciseNow = self.timeUtil.conciseNow()

            dumpName = "%s_%s" % (conciseNow, db)

            command = """pg_dump -h %s %s > %s/%s.sql""" % (host, db,
                                                            self.configer
                                                            .configOptionValue(
                                                                'Export',
                                                                'db_export_path'),
                                                            dumpName)

            fullPath = '%s/%s.sql' % (
                self.configer.configOptionValue('Export', 'db_export_path'),
                dumpName)

            self.logger.log('fullPath: %s' % fullPath, 'DEBUG')

            try:
                if localExport:
                    # Generate the SQL script export.
                    subprocess.check_call(command, shell = True)
            except subprocess.CalledProcessError, e:
                self.logger.log("Exception while dumping: %s" % e)
                noErrors = False

            # Obtain the checksum for the export prior to compression.
            md5sum1 = self.fileUtil.md5Checksum(fullPath)

            try:
                self.logger.log("mtime: %s, md5sum1: %s" % (
                    time.ctime(os.path.getmtime(fullPath)), md5sum1), 'INFO')
            except OSError as detail:
                self.logger.log('Exception while accessing %s.' % fullPath,
                                'ERROR')

            # Perform compression of the file.
            self.logger.log("Compressing %s using gzip." % db, 'info')
            self.logger.log('fullpath: %s' % fullPath, 'DEBUG')

            self.fileUtil.gzipCompressFile(fullPath)
            compressedFullPath = '%s%s' % (fullPath, '.gz')

            # Verify the compressed file by uncompressing it and verifying its
            # checksum against the original checksum.
            self.logger.log('reading: %s' % compressedFullPath, 'DEBUG')
            self.logger.log('writing: %s' % os.path.join(
                self.configer.configOptionValue('Testing',
                                                'export_test_data_path'),
                os.path.splitext(os.path.basename(fullPath))[0]), 'DEBUG')

            # Gzip uncompress and verify by checksum is disabled until a more
            # efficient, non-memory-based, uncompress is implemented.

            GZIP_UNCOMPRESS_FILE = False
            if GZIP_UNCOMPRESS_FILE:
                self.fileUtil.gzipUncompressFile(compressedFullPath,
                                                 os.path.join(
                                                     self.configer
                                                     .configOptionValue(
                                                         'Testing',
                                                         'export_test_data_path'),
                                                     fullPath))

            time.sleep(1)

            VERIFY_BY_CHECKSUM = False
            if VERIFY_BY_CHECKSUM:
                md5sum2 = self.fileUtil.md5Checksum(fullPath)

                self.logger.log("mtime: %s, md5sum2: %s" % (
                    time.ctime(os.path.getmtime(fullPath)), md5sum2), 'INFO')

                if md5sum1 == md5sum2:
                    self.logger.log(
                        'Compressed file has been validated by checksum.',
                        'INFO')
                else:
                    noErrors = False

            if toCloud:
                if numChunks != 0:
                    self.logger.log('Splitting %s' % compressedFullPath,
                                    'DEBUG')
                    filesToUpload = self.fileUtil.splitLargeFile(
                        fullPath = compressedFullPath, chunkSize = chunkSize,
                        numChunks = self.numberOfChunksToUse(fullPath))
                    if not filesToUpload:
                        raise (Exception, 'Exception during file splitting.')
                    self.logger.log('to upload: %s' % filesToUpload, 'debug')
                else:
                    filesToUpload = [compressedFullPath]

                # Upload the files to the cloud.

                self.logger.log('files to upload: %s' % filesToUpload, 'debug')
                for f in filesToUpload:
                    self.logger.log('Uploading %s.' % f, 'info')
                    fileID = self.uploadDBToCloudStorage(f, testing = testing)
                    self.addReaders(fileID,
                                    self.configer.configOptionValue().split(
                                        ','))

            # Remove the uncompressed file.
            try:
                if not testing:
                    os.remove('%s' % fullPath)
            except OSError as e:
                self.logger.log(
                    'Exception while removing %s: %s.' % (fullPath, e))
                noErrors = False

        # End for db in databases.

        self.deleteOutdatedFiles(minAge = datetime.timedelta(days = int(
            self.configer.configOptionValue('Export', 'days_to_keep'))))

        return noErrors


    def numberOfChunksToUse(self, fullPath):
        """
        Return the number of chunks to be used by the file splitter based on
        the file size of the file at fullPath.
        :param fullPath
        :returns: Number of chunks to create.
        """

        fsize = os.path.getsize(fullPath)
        self.logger.log('fullpath: %s, fsize: %s' % (fullPath, fsize))
        if (fsize >= self.configer.configOptionValue('Export',
                                                     'max_bytes_before_split')):
            return self.configer.configOptionValue('Export',
                                                   'num_split_sections')
        return 1


    def uploadDBToCloudStorage(self, fullPath = '', testing = False):
        """
        Export a DB to cloud storage.

        :param fullPath of DB file to be exported.
        :param testing: When to to True, Testing Mode is used.
        :returns: True on verified on upload; False if verification fails.
        """

        success = True
        dbName = os.path.basename(fullPath)

        self.logger.log('full path %s' % os.path.dirname(fullPath), 'DEBUG')
        self.logger.log("Uploading %s." % dbName)

        try:
            media_body = MediaFileUpload(fullPath,
                                         mimetype =
                                         'application/gzip-compressed',
                                         resumable = True)
            body = {'title': dbName,
                    'description': 'Hawaii Smart Energy Project gzip '
                                   'compressed DB export.',
                    'mimeType': 'application/gzip-compressed'}

            result = self.driveService.files().insert(body = body,
                                                      media_body =
                                                      media_body).execute()

        except (errors.ResumableUploadError, BadStatusLine) as detail:
            # Upload failures can result in a BadStatusLine.
            self.logger.log(
                "Exception while uploading %s: %s." % (dbName, detail), 'error')
            success = False

        if not self.verifyMD5Sum(fullPath, self.fileIDForFileName(dbName)):
            self.logger.log('Failed MD5 checksum verification.', 'INFO')
            success = False

        if success:
            self.logger.log('Verification by MD5 checksum succeeded.', 'INFO')
            self.logger.log("Finished.")
        return success


    def retrieveCredentials(self):
        """
        Perform authorization at the server.

        Credentials are loaded into the object attribute googleAPICredentials.
        """

        flow = OAuth2WebServerFlow(self.clientID, self.clientSecret,
                                   self.oauthScope, self.oauthConsent)
        authorize_url = flow.step1_get_authorize_url()
        print 'Go to the following link in your browser: ' + authorize_url
        code = raw_input('Enter verification code: ').strip()
        self.googleAPICredentials = flow.step2_exchange(code)

        print "refresh_token = %s" % self.googleAPICredentials.refresh_token
        print "expiry = %s" % self.googleAPICredentials.token_expiry


    def freeSpace(self):
        """
        Get free space from the drive service.

        :param driveService: Object for the drive service.
        :returns: Free space on the drive service as an integer.
        """

        aboutData = self.driveService.about().get().execute()
        return int(aboutData['quotaBytesTotal']) - int(
            aboutData['quotaBytesUsed']) - int(
            aboutData['quotaBytesUsedInTrash'])


    def deleteFile(self, fileID = ''):
        """
        Delete the file with ID fileID.

        :param fileID: Googe API file ID.
        """

        self.logger.log('Deleting file with file ID: %s' % fileID, 'debug')

        try:
            self.driveService.files().delete(fileId = fileID).execute()

        except errors.HttpError, error:
            self.logger.log('Exception while deleting: %s' % error, 'error')


    def deleteOutdatedFiles(self, minAge = datetime.timedelta(days = 0),
                            maxAge = datetime.timedelta(weeks = 9999999)):
        """
        Remove outdated files from cloud storage.

        :param minAge: Minimum age before a file is considered outdated.
        :param maxAge: Maximum age to consider for a file.
        :returns: Count of deleted items.
        """

        deleteCnt = 0

        if minAge == datetime.timedelta(days = 0):
            return 0

        for item in self.cloudFiles['items']:
            t1 = datetime.datetime.strptime(item['createdDate'],
                                            "%Y-%m-%dT%H:%M:%S.%fZ")
            self.logger.log(
                't1: %s' % datetime.datetime.strftime(t1, '%Y-%m-%d %H:%M:%S'),
                'debug')
            t2 = datetime.datetime.now()
            tdelta = t2 - t1
            self.logger.log('tdelta: %s' % tdelta, 'debug')
            if tdelta > minAge and tdelta < maxAge:
                deleteCnt += 1
                self.deleteFile(fileID = item['id'])

        return deleteCnt


    def sendNotificationOfFiles(self):
        """
        Provide a notification that lists the export files along with sharing
        links.
        """

        pass


    def listOfDownloadableFiles(self):
        """
        Create a list of downloadable files.
        """

        files = []

        for i in self.cloudFiles['items']:
            item = dict()
            item['title'] = i['title']
            item['webContentLink'] = i['webContentLink']
            item['id'] = i['id']
            item['createdDate'] = i['createdDate']
            item['fileSize'] = i['fileSize']
            files.append(item)

        return files


    def verifyMD5Sum(self, localFilePath, remoteFileID):
        """
        Verify that the local MD5 sum matches the MD5 sum for the remote file
        corresponding to an ID.

        This verifies that the uploaded file matches the local compressed
        export file.

        :param localFilePath: Full path of the local file.
        :param remoteFileID: Cloud ID for the remote file.
        :returns: True if the MD5 sums match, otherwise, False.
        """

        self.logger.log('local file path: %s' % localFilePath)
        # Get the md5sum for the local file.
        f = open(localFilePath, mode = 'rb')
        fContent = hashlib.md5()
        for buf in iter(partial(f.read, 128), b''):
            fContent.update(buf)
        localMD5Sum = fContent.hexdigest()
        f.close()

        self.logger.log('local md5: %s' % localMD5Sum, 'DEBUG')

        # Get the MD5 sum for the remote file.
        for item in self.cloudFiles['items']:
            if (item['id'] == remoteFileID):
                self.logger.log('remote md5: %s' % item['md5Checksum'], 'DEBUG')
                if localMD5Sum == item['md5Checksum']:
                    return True
                else:
                    return False
        return False


    def fileIDForFileName(self, filename):
        """
        Get the file ID for the given filename.

        This method supports matching multiple matching cloud filenames but only
        returns the ID for a single matching filename.

        This not the best way to handle things, but it works for the typical
        use case and prevents errors from taking down the system.

        :param Filename for which to retrieve the ID.
        :returns: A cloud file ID.
        """

        ids = []

        for item in self.cloudFiles['items']:

            if (item['title'] == filename):
                # self.logger.log('item: %s' % item, 'INFO')
                # self.logger.log('matching title: %s' % item['title'], 'DEBUG')
                # self.logger.log(
                #     'file state trashed: %s' % item['labels']['trashed'],
                #     'DEBUG')
                if not item['labels']['trashed']:
                    ids.append(item['id'])

        if ids:
            return ids[0]
        elif not ids:
            return None
        else:
            raise Exception("Unmatched case for fileIDForFileName.")


    def addReaders(self, fileID = None, emailAddressList = None):
        """
        Add reader permission to an export file for the given list of email
        addresses.

        Email notification is suppressed by default.

        :param fileID: Cloud file ID to be processed.
        :param emailAddressList: A list of email addresses.
        :returns: True if successful, otherwise False.
        """

        success = True

        for addr in emailAddressList:
            permission = {'value': addr, 'type': 'user', 'role': 'reader'}

            if fileID:
                try:
                    resp = self.driveService.permissions().insert(
                        fileId = fileID, sendNotificationEmails = False,
                        body = permission).execute()
                except errors.HttpError, error:
                    print 'An error occurred: %s' % error
                    success = False

        return success

