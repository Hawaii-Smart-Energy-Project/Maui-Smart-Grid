# !/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'
__copyright__ = 'Copyright (c) 2014, University of Hawaii Smart Energy Project'
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
import requests
from StringIO import StringIO
from requests.adapters import SSLError
import shutil
from msg_db_connector import MSGDBConnector
from msg_db_util import MSGDBUtil


class MSGDBExporter(object):
    """
    Export MSG DBs as SQL scripts.

    Supports export to local storage and to cloud storage.

    Usage:

    from msg_db_exporter import MSGDBExporter
    exporter = MSGDBExporter()

    Public API:

    exportDB(databases:List, 
             toCloud:Boolean, 
             testing:Boolean,
             numChunks:Integer, 
             deleteOutdated:Boolean): Export a list of DBs to the cloud.
    """

    # List of cloud files.
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
        storage = Storage(
            '{}/google_api_credentials'.format(self.credentialPath))

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

        self.logger = MSGLogger(__name__, 'DEBUG', useColor = False)
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
        self.exportTempWorkPath = self.configer.configOptionValue('Export',
                                                                  'db_export_work_path')

        self.credentialPath = self.configer.configOptionValue('Export',
                                                              'google_api_credentials_path')
        self.credentialStorage = Storage(
            '{}/google_api_credentials'.format(self.credentialPath))

        self._driveService = None
        self._cloudFiles = None
        self.postAgent = 'Maui Smart Grid 1.0.0 DB Exporter'


    def verifyExportChecksum(self, testing = False):
        """
        Verify the compressed export file using a checksum.

        * Save the checksum of the original uncompressed export data.
        * Extract the compressed file.
        * Verify the uncompressed export data.

        :param testing: When set to True, Testing Mode is used.
        """

        # Get the checksum of the original file.
        md5sum = self.fileUtil.md5Checksum(self.exportTempWorkPath)
        self.logger.log('md5sum: {}'.format(md5sum))


    def db_username(self):
        return "postgres"
        # return self.configer.configOptionValue('Database', 'db_username')

    def db_password(self):
        return self.configer.configOptionValue('Database', 'db_password')

    def db_port(self):
        return self.configer.configOptionValue('Database', 'db_port')


    def dumpCommand(self, db = '', dumpName = ''):
        """
        This method makes use of

        pg_dump -s -p ${PORT}
                   -U ${USERNAME}
                   [-T ${OPTIONAL_TABLE_EXCLUSIONS}]
                   ${DB_NAME} >
                   ${EXPORT_TEMP_WORK_PATH}/${DUMP_TIMESTAMP}_{DB_NAME}.sql

        :param db: String
        :param dumpName: String
        :return: String of command used to export DB.
        """

        # For reference only:
        # Password is passed from ~/.pgpass.
        # Note that ':' and '\' characters should be escaped with '\'.
        # Ref: http://www.postgresql.org/docs/9.1/static/libpq-pgpass.html

        # Dump databases as the superuser. This method does not require a
        # stored password when running under a root crontab.
        if not db or not dumpName:
            raise Exception('DB and dumpname required.')

        # Process exclusions.

        exclusions = self.dumpExclusionsDictionary()
        excludeList = []
        if db in exclusions:
            excludeList = exclusions[db]
        excludeString = ''
        if len(excludeList) > 0 and exclusions != None:
            for e in excludeList:
                excludeString += """-T '"{}"' """.format(e)

        return 'sudo -u postgres pg_dump -p {0} -U {1} {5} {2} > {3}/{4}' \
               '.sql'.format(self.db_port(), self.db_username(), db,
                             self.exportTempWorkPath, dumpName, excludeString)


    def dumpExclusionsDictionary(self):
        """
        :param db: String of DB name for which to retrieve exclusions.
        :return: Dictionary with keys as DBs and values as lists of tables to
        be excluded for a given database.
        """
        try:
            if type(eval(self.configer.configOptionValue('Export',
                                                         'db_export_exclusions'))) == type(
                    {}):
                return eval(self.configer.configOptionValue('Export',
                                                            'db_export_exclusions'))
            else:
                return None
        except SyntaxError as detail:
            self.logger.log(
                'SyntaxError exception while getting exclusions: {}'.format(
                    detail))


    def dumpName(self, db = ''):
        """
        :param db: String
        :return: String of file name used for dump file of db.
        """
        if not db:
            raise Exception('DB required.')
        return "{}_{}".format(self.timeUtil.conciseNow(), db)


    def filesToUpload(self, compressedFullPath = '', numChunks = 0,
                      chunkSize = 0):
        """
        :param compressedFullPath: String
        :param numChunks: Int
        :param chunkSize: Int
        :return: List of files to be uploaded according to their split
        sections, if applicable.
        """
        if numChunks != 0:
            self.logger.log('Splitting {}'.format(compressedFullPath), 'DEBUG')

            filesToUpload = self.fileUtil.splitLargeFile(
                fullPath = compressedFullPath, chunkSize = chunkSize,
                numChunks = numChunks)

            if not filesToUpload:
                raise Exception('Exception during file splitting.')
            else:
                self.logger.log('to upload: {}'.format(filesToUpload), 'debug')
                return filesToUpload

        else:
            return [compressedFullPath]

    def dumpResult(self, db = '', dumpName = '', fullPath = ''):
        """
        :param dumpName: String of filename of dump file.
        :param fullPath: String of full path to dump file.
        :return: Boolean True if dump operation was successful, otherwise False.
        """

        success = False

        self.logger.log('fullPath: {}'.format(fullPath), 'DEBUG')

        try:
            # Generate the SQL script export.
            self.logger.log('cmd: {}'.format(
                self.dumpCommand(db = db, dumpName = dumpName)))
            subprocess.check_call(
                self.dumpCommand(db = db, dumpName = dumpName), shell = True)
        except subprocess.CalledProcessError as error:
            self.logger.log("Exception while dumping: {}".format(error))
            success = False

        return success

    def exportDB(self, databases = None, toCloud = False, localExport = True,
                 testing = False, chunkSize = 0, numChunks = 0,
                 deleteOutdated = False):
        """
        Export a set of DBs to local storage.

        :param databases: List of database names that will be exported.
        :param toCloud: Boolean if set to True, then the export will also be
        copied to cloud storage.
        :param localExport: Boolean when set to True, the DB is exported
        locally.
        :param testing: Boolean flag for testing mode. (@DEPRECATED)
        :param chunkSize: Integer size in bytes of chunk size used for
        splitting.
        :param deleteOutdated: Boolean indicating outdated files in the cloud
        should be removed.
        :returns: Boolean True if no errors have occurred, False otherwise.
        """

        noErrors = True

        for db in databases:
            self.logger.log('Exporting {} using pg_dump.'.format(db), 'info')

            dumpName = self.dumpName(db = db)
            fullPath = '{}/{}.sql'.format(self.exportTempWorkPath, dumpName)
            if localExport:
                noErrors = self.dumpResult(db, dumpName, fullPath)

            # Perform compression of the file.
            self.logger.log("Compressing {} using gzip.".format(db), 'info')
            self.logger.log('fullpath: {}'.format(fullPath), 'DEBUG')

            gzipResult = self.fileUtil.gzipCompressFile(fullPath)
            compressedFullPath = '{}{}'.format(fullPath, '.gz')
            numChunks = self.numberOfChunksToUse(compressedFullPath)
            time.sleep(1)

            # Gzip uncompress and verify by checksum is disabled until a more
            # efficient, non-memory-based, uncompress is implemented.
            # md5sum1 = self.fileUtil.md5Checksum(fullPath)
            # self.md5Verification(compressedFullPath=compressedFullPath,
            # fullPath=fullPath,md5sum1=md5sum1)

            if toCloud:
                # Split compressed files into a set of chunks to improve the
                # reliability of uploads.

                # Upload the files to the cloud.
                for f in self.filesToUpload(
                        compressedFullPath = compressedFullPath,
                        numChunks = numChunks, chunkSize = chunkSize):
                    self.logger.log('Uploading {}.'.format(f), 'info')
                    fileID = self.uploadFileToCloudStorage(fullPath = f,
                                                           testing = testing)

                    # @todo Provide support for a retry count.
                    if not fileID:
                        self.logger.log('Retrying upload of {}.'.format(f),
                                        'warning')
                        time.sleep(10)
                        fileID = self.uploadFileToCloudStorage(fullPath = f,
                                                               testing =
                                                               testing)

                    self.logger.log('file id after upload: {}'.format(fileID))

                    if fileID != None:
                        if not self.addReaders(fileID,
                                               self.configer.configOptionValue(
                                                       'Export',
                                                       'read_permission').split(
                                                       ',')):
                            time.sleep(10)
                            self.logger.log(
                                'Retrying adding readers for {}.'.format(f),
                                'warning')

                            # @todo Provide support for retry count.
                            if not self.addReaders(fileID,
                                                   self.configer.configOptionValue(
                                                           'Export',
                                                           'read_permission').split(
                                                           ',')):
                                self.logger.log(
                                    'Failed to add readers for {}.'.format(f),
                                    'error')
                        self.logSuccessfulExport(*self.metadataOfFileID(fileID))

                    # Remove split sections if they exist.
                    try:
                        if not testing and numChunks > 1:
                            self.logger.log('Removing {}'.format(f))
                            os.remove('{}'.format(f))
                    except OSError as error:
                        self.logger.log(
                            'Exception while removing {}: {}.'.format(fullPath,
                                                                      error))
                        noErrors = False

            # End if toCloud.

            if gzipResult:
                self.moveToFinalPath(compressedFullPath = compressedFullPath)

            # Remove the uncompressed file.
            try:
                if not testing:
                    self.logger.log('Removing {}'.format(fullPath))
                    os.remove('{}'.format(fullPath))
            except OSError as error:
                self.logger.log(
                    'Exception while removing {}: {}.'.format(fullPath, error))
                noErrors = False

        # End for db in databases.

        if deleteOutdated:
            self.deleteOutdatedFiles(minAge = datetime.timedelta(days = int(
                self.configer.configOptionValue('Export', 'days_to_keep'))))

        return noErrors

    def moveToFinalPath(self, compressedFullPath = ''):
        """
        Move a compressed final to the final export path.
        :param compressedFullPath: String for the compressed file.
        :return:
        """
        self.logger.log('Moving {} to final path.'.format(compressedFullPath),
                        'debug')
        try:
            shutil.move(compressedFullPath,
                        self.configer.configOptionValue('Export',
                                                        'db_export_final_path'))
        except Exception as detail:
            self.logger.log(
                'Exception while moving {} to final export path: {}'.format(
                    compressedFullPath, detail), 'error')


    def md5Verification(self, compressedFullPath = '', fullPath = '',
                        md5sum1 = ''):
        """
        Perform md5 verification of a compressed file at compressedFullPath
        where the original file is at fullPath and has md5sum1.

        :param compressedFullPath: String
        :param fullPath: String
        :param md5sum1: String of md5sum of source file.
        :return:
        """

        GZIP_UNCOMPRESS_FILE = False
        if GZIP_UNCOMPRESS_FILE:
            # Verify the compressed file by uncompressing it and
            # verifying its
            # checksum against the original checksum.
            self.logger.log('reading: {}'.format(compressedFullPath), 'DEBUG')
            self.logger.log('writing: {}'.format(os.path.join(
                self.configer.configOptionValue('Testing',
                                                'export_test_data_path'),
                os.path.splitext(os.path.basename(fullPath))[0])), 'DEBUG')

            self.fileUtil.gzipUncompressFile(compressedFullPath, os.path.join(
                self.configer.configOptionValue('Testing',
                                                'export_test_data_path'),
                fullPath))

        VERIFY_BY_CHECKSUM = False
        if VERIFY_BY_CHECKSUM:
            md5sum2 = self.fileUtil.md5Checksum(fullPath)

            self.logger.log("mtime: {}, md5sum2: {}".format(
                time.ctime(os.path.getmtime(fullPath)), md5sum2), 'INFO')

            if md5sum1 == md5sum2:
                self.logger.log(
                    'Compressed file has been validated by checksum.', 'INFO')
            else:
                noErrors = False

    def numberOfChunksToUse(self, fullPath):
        """
        Return the number of chunks to be used by the file splitter based on
        the file size of the file at fullPath.
        :param fullPath: String
        :returns: Int Number of chunks to create.
        """

        fsize = os.path.getsize(fullPath)
        self.logger.log('fullpath: {}, fsize: {}'.format(fullPath, fsize))
        if (fsize >= int(self.configer.configOptionValue('Export',
                                                         'max_bytes_before_split'))):
            # Note that this does not make use of the remainder in the division.
            chunks = int(fsize / int(self.configer.configOptionValue('Export',
                                                                     'max_bytes_before_split')))
            self.logger.log('Will split with {} chunks.'.format(chunks))
            return chunks
        self.logger.log('Will NOT split file.', 'debug')
        return 1


    def uploadFileToCloudStorage(self, fullPath = '', retryCount = 0,
                                 testing = False):
        """
        Export a file to cloud storage.

        :param fullPath: String of file to be exported.
        :param testing: Boolean when set to True, Testing Mode is used.
        :param retryCount: Int of number of times to retry the upload if
        there is a failure.
        :returns: String File ID on verified on upload; None if verification
        fails.
        """

        # @todo Implement retry count.

        success = True
        myFile = os.path.basename(fullPath)

        self.logger.log(
            'full path {}'.format(os.path.dirname(fullPath), 'DEBUG'))
        self.logger.log("Uploading {}.".format(myFile))

        result = {}
        try:
            media_body = MediaFileUpload(fullPath,
                                         mimetype =
                                         'application/gzip-compressed',
                                         resumable = True)
            body = {'title': myFile,
                    'description': 'Hawaii Smart Energy Project gzip '
                                   'compressed DB export.',
                    'mimeType': 'application/gzip-compressed'}

            # Result is a Files resource.
            result = self.driveService.files().insert(body = body,
                                                      media_body =
                                                      media_body).execute()

        except Exception as detail:
            # Upload failures can result in a BadStatusLine.
            self.logger.log(
                "Exception while uploading {}: {}.".format(myFile, detail),
                'error')
            success = False

        if not self.__verifyMD5Sum(fullPath, self.fileIDForFileName(myFile)):
            self.logger.log('Failed MD5 checksum verification.', 'INFO')
            success = False

        if success:
            self.logger.log('Verification by MD5 checksum succeeded.', 'INFO')
            self.logger.log("Finished.")

        if not success:
            return None

        return result['id']


    def __retrieveCredentials(self):
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

        print "refresh_token = {}".format(
            self.googleAPICredentials.refresh_token)
        print "expiry = {}".format(self.googleAPICredentials.token_expiry)


    def freeSpace(self):
        """
        Get free space from the drive service.

        :param driveService: Object for the drive service.
        :returns: Int of free space (bytes) on the drive service.
        """

        aboutData = self.driveService.about().get().execute()
        return int(aboutData['quotaBytesTotal']) - int(
            aboutData['quotaBytesUsed']) - int(
            aboutData['quotaBytesUsedInTrash'])


    def deleteFile(self, fileID = ''):
        """
        Delete the file with ID fileID.

        :param fileID: String of a Google API file ID.
        """

        # @todo Report the filename.
        self.logger.log('Deleting file with file ID: {}'.format(fileID),
                        'debug')

        try:
            self.driveService.files().delete(fileId = fileID).execute()

        except errors.HttpError as error:
            self.logger.log('Exception while deleting: {}'.format(error),
                            'error')


    def deleteOutdatedFiles(self, minAge = datetime.timedelta(days = 0),
                            maxAge = datetime.timedelta(weeks = 9999999)):
        """
        Remove outdated files from cloud storage.

        :param minAge: datetime.timedelta in days of the minimum age before a
        file is considered outdated.
        :param maxAge: datetime.timedelta in days of the maximum age to
        consider for a file.
        :returns: Int count of deleted items.
        """

        self.logger.log('Deleting outdated.', 'DEBUG')
        deleteCnt = 0

        if minAge == datetime.timedelta(days = 0):
            return 0

        for item in self.cloudFiles['items']:
            t1 = datetime.datetime.strptime(item['createdDate'],
                                            "%Y-%m-%dT%H:%M:%S.%fZ")
            self.logger.log('t1: {}'.format(t1.strftime('%Y-%m-%d %H:%M:%S')),
                            'debug')
            t2 = datetime.datetime.now()
            tdelta = t2 - t1
            self.logger.log(
                'tdelta: {}, min age: {}, max age: {}'.format(tdelta, minAge,
                                                              maxAge), 'debug')
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


    def sendDownloadableFiles(self):
        """
        Send available files via HTTP POST.
        :returns: None
        """

        myPath = '{}/{}'.format(self.exportTempWorkPath,
                                'list-of-downloadable-files.txt')

        fp = open(myPath, 'wb')

        output = StringIO()
        output.write(self.markdownListOfDownloadableFiles())

        fp.write(self.markdownListOfDownloadableFiles())
        fp.close()

        headers = {'User-Agent': self.postAgent, 'Content-Type': 'text/html'}
        try:
            r = requests.post(self.configer.configOptionValue('Export',
                                                              'export_list_post_url'),
                              output.getvalue(), headers = headers)
            print 'text: {}'.format(r.text)
        except requests.adapters.SSLError as error:
            # @todo Implement alternative verification.
            self.logger.log('SSL error: {}'.format(error), 'error')

        output.close()


    def metadataOfFileID(self, fileID = ''):
        """
        :param fileID: String of a file ID in the cloud.
        :return: Tuple of metadata (name, url, timestamp, size) for a given
        file ID.
        """
        item = [i for i in self.cloudFiles['items'] if i['id'] == fileID][0]
        return (item[u'originalFilename'], item[u'webContentLink'],
                item[u'createdDate'], item[u'fileSize'])


    def listOfDownloadableFiles(self):
        """
        Create a list of downloadable files.
        :returns: List of dicts of files that are downloadable from the cloud.
        """

        files = []
        for i in reversed(sorted(self.cloudFiles['items'],
                                 key = lambda k: k['createdDate'])):
            item = dict()
            item['title'] = i['title']
            item['webContentLink'] = i['webContentLink']
            item['id'] = i['id']
            item['createdDate'] = i['createdDate']
            item['fileSize'] = i['fileSize']
            files.append(item)
        return files


    def markdownListOfDownloadableFiles(self):
        """
        Generate content containing a list of downloadable files in Markdown
        format.

        :returns: String content in Markdown format.
        """

        content = "||*Name*||*Created*||*Size*||\n"
        for i in self.listOfDownloadableFiles():
            content += "||[`{}`]({})".format(i['title'], i['webContentLink'])
            content += "||`{}`".format(i['createdDate'])
            content += "||`{} B`||".format(int(i['fileSize']))
            content += '\n'

        self.logger.log('content: {}'.format(content))

        return content

    def plaintextListOfDownloadableFiles(self):
        """
        Generate content containing a list of downloadable files in plaintext
        format.

        :returns: String content as plaintext.
        """
        content = ''
        for i in self.listOfDownloadableFiles():
            content += "{}, {}, {}, {} B\n".format(i['title'],
                                                   i['webContentLink'],
                                                   i['createdDate'],
                                                   int(i['fileSize']))

        self.logger.log('content: {}'.format(content))

        return content

    def logSuccessfulExport(self, name = '', url = '', datetime = 0, size = 0):
        """
        When an export has been successful, log information about the export
        to the database.

        The items to log include:
        * filename
        * URL
        * timestamp
        * filesize

        :param name: String
        :param url: String
        :param datetime:
        :param size: Int
        :return: True if no errors occurred, else False.
        """

        def exportHistoryColumns():
            return ['name', 'url', 'timestamp', 'size']

        timestamp = lambda \
                datetime: 'to_timestamp(0)' if datetime == 0 else "timestamp " \
                                                                  "'{}'".format(
            datetime)

        sql = 'INSERT INTO "{0}" ({1}) VALUES ({2}, {3}, {4}, {5})'.format(
            self.configer.configOptionValue('Export', 'export_history_table'),
            ','.join(exportHistoryColumns()), "'" + name + "'", "'" + url + "'",
            timestamp(datetime), size)

        conn = MSGDBConnector().connectDB()
        cursor = conn.cursor()
        dbUtil = MSGDBUtil()
        result = dbUtil.executeSQL(cursor, sql, exitOnFail = False)
        conn.commit()
        return result


    def __verifyMD5Sum(self, localFilePath, remoteFileID):
        """
        Verify that the local MD5 sum matches the MD5 sum for the remote file
        corresponding to an ID.

        This verifies that the uploaded file matches the local compressed
        export file.

        :param localFilePath: String of the full path of the local file.
        :param remoteFileID: String of the cloud ID for the remote file.
        :returns: Boolean True if the MD5 sums match, otherwise, False.
        """

        self.logger.log('remote file ID: {}'.format(remoteFileID))
        self.logger.log('local file path: {}'.format(localFilePath))

        # Get the md5sum for the local file.
        f = open(localFilePath, mode = 'rb')
        fContent = hashlib.md5()
        for buf in iter(partial(f.read, 128), b''):
            fContent.update(buf)
        localMD5Sum = fContent.hexdigest()
        f.close()

        self.logger.log('local md5: {}'.format(localMD5Sum), 'DEBUG')

        def verifyFile():
            # Get the MD5 sum for the remote file.
            for item in self.cloudFiles['items']:
                if (item['id'] == remoteFileID):
                    self.logger.log(
                        'remote md5: {}'.format(item['md5Checksum']), 'DEBUG')
                    if localMD5Sum == item['md5Checksum']:
                        return True
                    else:
                        return False

        try:
            if verifyFile():
                return True
            else:
                return False

        except errors.HttpError as detail:
            self.logger.log('HTTP error during MD5 verification.', 'error')

            time.sleep(10)

            if verifyFile():
                return True
            else:
                return False


    def fileIDForFileName(self, filename):
        """
        Get the file ID for the given filename.

        This method supports matching multiple matching cloud filenames but only
        returns the ID for a single matching filename.

        This not the best way to handle things, but it works for the typical
        use case and prevents errors from taking down the system.

        :param String of the filename for which to retrieve the ID.
        :returns: String of a cloud file ID.
        """

        ids = []

        for item in self.cloudFiles['items']:

            if (item['title'] == filename):

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

        :param fileID: String of the cloud file ID to be processed.
        :param emailAddressList: List of email addresses.
        :returns: Boolean True if successful, otherwise False.
        """

        success = True

        self.logger.log('file id: {}'.format(fileID))
        self.logger.log('address list: {}'.format(emailAddressList))

        for addr in emailAddressList:
            permission = {'value': addr, 'type': 'user', 'role': 'reader'}

            if fileID:
                try:
                    resp = self.driveService.permissions().insert(
                        fileId = fileID, sendNotificationEmails = False,
                        body = permission).execute()
                    self.logger.log(
                        'Reader permission added for {}.'.format(addr))
                except errors.HttpError as error:
                    self.logger.log('An error occurred: {}'.format(error))
                    success = False

        return success
