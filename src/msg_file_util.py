#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'
__copyright__ = 'Copyright (c) 2013, University of Hawaii Smart Energy Project'
__license__ = 'https://raw.github' \
              '.com/Hawaii-Smart-Energy-Project/Maui-Smart-Grid/master/BSD' \
              '-LICENSE.txt'

from msg_logger import MSGLogger
import hashlib
from functools import partial
import gzip
import os


class MSGFileUtil(object):
    """
    Utilities related to files and directories.
    """

    def __init__(self):
        """
        Constructor.
        """
        self.logger = MSGLogger(__name__, 'DEBUG')


    def validDirectory(self, path):
        """
        Verify that the path is a valid directory.

        :param path: Path to check.
        :returns: True if path is a valid directory.
        """

        if os.path.exists(path) and os.path.isdir(path):
            return True
        else:
            return False


    def md5Checksum(self, fullPath):
        """
        Get the MD5 checksum for the file given by fullPath.

        :param fullPath: Full path of the file to generate for which to
        generate a checksum.
        :returns: MD5 checksum value as a hex digest.
        """

        try:
            f = open(fullPath, mode = 'rb')
            content = hashlib.md5()
            for buf in iter(partial(f.read, 128), b''):
                content.update(buf)
            md5sum = content.hexdigest()
            f.close()
            return md5sum
        except IOError as detail:
            self.logger.log(
                'Exception during checksum calculation: %s' % detail, 'ERROR')


    def gzipUncompressFile(self, srcPath, destPath):
        """
        Gzip uncompress a file given by fullPath.

        :param srcPath: Full path of the file to be uncompressed.
        :param destPath: Full path of file to be written to.
        """

        self.logger.log('Writing to %s' % destPath, 'DEBUG')
        gzipFile = gzip.open(srcPath, "rb")
        uncompressedFile = open(destPath, "wb")
        decoded = gzipFile.read()
        try:
            uncompressedFile.write(decoded)
        except:
            self.logger.log("Exception while writing uncompressed file.")
        gzipFile.close()
        uncompressedFile.close()


    def gzipCompressFile(self, fullPath):
        """
        Perform gzip compression on a file at fullPath.

        @todo Generalize this method.

        :param fullPath: Full path of the file to be compressed. The full
        path is mislabeled here and refers to the full path minus the
        extension of the data to be compressed.
        """

        try:
            f_in = open('%s' % (fullPath), 'rb')
            f_out = gzip.open('%s.gz' % (fullPath), 'wb')
            f_out.writelines(f_in)
            f_out.close()
            f_in.close()
        except IOError as detail:
            self.logger.log('Exception while gzipping: %s' % detail, 'ERROR')


    def splitFile(self, fullPath = '', chunkSize = 0):
        """
        Split a file into chunks. Write output files to base path of the
        input file.

        Adapted from https://gist.github.com/mattiasostmar/7883550.

        :param fullPath:
        :param chunkSize:
        :returns: number of chunks
        """

        basePath = os.path.dirname(fullPath)
        baseName = os.path.basename(fullPath)

        f = open(fullPath, 'rb')
        data = f.read()
        f.close()

        bytes = len(data)

        # Ensure splitting doesn't happen if it's not needed.
        if bytes <= chunkSize:
            return 0

        # Calculate the number of chunks to be created.
        numChunks = bytes / chunkSize
        if (bytes % chunkSize):
            numChunks += 1

        chunkNames = []

        fCnt = 0
        for i in range(0, bytes + 1, chunkSize):
            fn1 = "%s/%s.%s" % (basePath, baseName, fCnt)
            print "writing to %s" % fn1
            chunkNames.append(fn1)

            try:
                f = open(fn1, 'wb')
                f.write(data[i:i + chunkSize])
                f.close()
            except Exception as detail:
                print "Exception during writing split file: %s" % detail

            fCnt += 1

        return numChunks
