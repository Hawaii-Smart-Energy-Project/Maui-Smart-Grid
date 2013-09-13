#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

Parallelized weather retrieval and processing.

@todo Convert fully to class versus the current hybrid implementation.

There are two types of retrieval, Primary and Secondary.

Primary retrieval makes use of a list of files matching a pattern given in
the configuration.

Secondary retrieval makes use of something that I am calling the Keep List.
It is intended for re-downloading files that already exist to get updated
data from the last insertion time.

This can involve, in regular use, re-downloading the previous month of data
and the current month of data.
"""

__author__ = 'Daniel Zhang (張道博)'
__copyright__ = 'Copyright (c) 2013, University of Hawaii Smart Energy Project'
__license__ = 'https://raw.github' \
              '.com/Hawaii-Smart-Energy-Project/Maui-Smart-Grid/master/BSD' \
              '-LICENSE.txt'

import pycurl
from msg_configer import MSGConfiger
from msg_logger import MSGLogger
import multiprocessing
import zipfile
import os.path
import os
import gzip
from msg_noaa_weather_data_util import MSGWeatherDataUtil
from msg_db_connector import MSGDBConnector
import fnmatch

weatherDataPath = ''
retriever = None
downloadCount = 0

WEATHER_DATA_PATH = ''
MSG_BODY = ''

# @todo Remove use of global weather data path.

class MSGWeatherDataRetriever(object):
    """
    Retrieve national NOAA weather data relevant to the MSG project and save it
    to local storage in the path given in the configuration file for [Weather
     Data], weather_data_path.

    Unzip the retrieved data and recompress the hourly data using gzip.
    """

    def __init__(self):
        self.configer = MSGConfiger()
        self.pool = None
        self.fileList = []
        self.dateList = []
        self.weatherUtil = MSGWeatherDataUtil()

        global weatherDataPath
        weatherDataPath = self.configer.configOptionValue('Weather Data',
                                                          'weather_data_path')
        global weatherDataURL
        weatherDataURL = self.configer.configOptionValue('Weather Data',
                                                         'weather_data_url')

        global weatherDataPattern
        weatherDataPattern = self.configer.configOptionValue('Weather Data',
                                                             'weather_data_pattern')


    def fileExists(self, filename):
        # @todo Move to external module.
        try:
            with open(filename):
                return True

        except IOError, e:
            # self.logger.log("IO Error: %s" % e, 'error')
            return False

        return False

# ********** End Class **********

def fileExists(filename):
    # @todo Move to external module.
    try:
        with open(filename):
            return True

    except IOError, e:
        logger.log("%s" % e, 'info')
        return False

    return False


def unzipWorker(filename, forceDownload = False):
    """
    Perform decompression of downloaded files.

    :param filename
    :param forceDownload: A flag indicating that the download should override
     the default behavior of the script.
    """

    global MSG_BODY
    originalName = filename

    hourlyGzName = retriever.weatherUtil.datePart(
        filename = filename) + "hourly.txt.gz"
    if fileExists(hourlyGzName) and not forceDownload:
        msg = "%s already exists." % hourlyGzName
        print msg
        MSG_BODY += '%s\n' % msg
        return

    if (fileExists(filename)):
        msg = "Unzipping %s." % filename
        print msg
        MSG_BODY += '%s\n' % msg
        try:

            zfile = zipfile.ZipFile(filename)
            for name in zfile.namelist():
                (dirname, filename) = os.path.split(name)
                if not dirname == '':
                    msg = "Decompressing " + filename + " into " + dirname + "."
                    print msg
                    MSG_BODY += '%s\n' % msg
                else:
                    msg = "Decompressing " + filename + "."
                    print msg
                    MSG_BODY += '%s\n' % msg

                if not os.path.exists(dirname) and not dirname == '':
                    os.mkdir(dirname)
                fd = open(name, "w")
                fd.write(zfile.read(name))
                fd.close()

            hourlyName = retriever.weatherUtil.datePart(
                filename = originalName) + "hourly.txt"

            if fileExists(hourlyName):
                msg = "Hourly file exists. Compressing the hourly file with " \
                      "gzip."
                print msg
                MSG_BODY += '%s\n' % msg

                gzipCompressFile(hourlyName)
            else:
                msg = "Hourly file not found."
                print msg
                MSG_BODY += '%s\n' % msg

        except zipfile.BadZipfile:
            msg = "Bad zipfile %s." % originalName
            print msg
            MSG_BODY += '%s\n' % msg


def gzipCompressFile(filename):
    """
    Perform gzip compression on a given file.

    :param filename
    """

    # @todo Move to external module.
    f_in = open(filename, 'rb')
    f_out = gzip.open(filename + ".gz", 'wb')
    f_out.writelines(f_in)
    f_out.close()
    f_in.close()


def unzipFile(filename, forceDownload = False):
    """
    Unzip a given file.

    :param filename
    :param forceDownload
    """

    unzipWorker(filename, forceDownload)


def performDownloading(filename, forceDownload = False):
    """
    Perform downloading of weather data file with a given filename.
    Existing files will not be retrieved.

    :param filename
    :param forceDownload
    :returns: True for success, False otherwise.
    """
    global MSG_BODY
    logger.log('')

    if WEATHER_DATA_PATH == '':
        msg = "Working directory has not been given."
        print msg
        MSG_BODY += '%s\n' % msg
        return False

    success = True


    # Change working directory to download location.
    os.chdir(WEATHER_DATA_PATH)
    if os.getcwd() != WEATHER_DATA_PATH:
        msg = "Working directory does not match."
        print msg
        MSG_BODY += '%s\n' % msg

    if not fileExists(filename) or forceDownload:
        msg = "Performing download on " + filename
        print msg
        MSG_BODY += '%s\n' % msg

        fp = open(weatherDataPath + "/" + filename, "wb")
        curl = pycurl.Curl()
        curl.setopt(pycurl.URL, weatherDataURL + "/" + filename)
        curl.setopt(pycurl.WRITEDATA, fp)
        try:
            curl.perform()
        except pycurl.error, e:
            errorCode, errorText = e.args
            msg = 'Error during retrieval: code: %s, text: %s.' % (
                errorCode, errorText)
            logger.log(msg)
            MSG_BODY += '%s\n' % msg

            success = False
        curl.close()
        fp.close()

    if fileExists(filename) or forceDownload:
        unzipFile(filename, forceDownload)

    global downloadCount
    downloadCount += 1

    return success


def performDownloadingWithForcedDownload(filename):
    performDownloading(filename, forceDownload = True)

# Use case: Month changes from Aug to Sep.
# Last loaded date was in Aug.
# Downloader is going to get Sep, but not the rest of Aug.
# To get the remainder of Aug, force download on Aug.

def cleanUpTxtFiles():
    """
    Clean up unused txt files by deleting them from local storage.
    """

    global MSG_BODY
    patterns = ['*hourly.txt', '*daily.txt', '*monthly.txt', '*precip.txt',
                '*remarks.txt', '*station.txt']
    for root, dirs, filenames in os.walk(
            configer.configOptionValue('Weather Data', 'weather_data_path')):
        for pat in patterns:
            for filename in fnmatch.filter(filenames, pat):
                os.remove(filename)
                msg = "Removed %s." % filename
                print msg
                MSG_BODY += '%s\n' % msg


def saveRetrievalResults():
    """
    Save retrieval results stored in a global string.
    """

    global MSG_BODY
    global WEATHER_DATA_PATH
    fp = open('%s/retrieval-results.txt' % WEATHER_DATA_PATH, 'wb')
    fp.write(MSG_BODY)
    fp.close()


if __name__ == '__main__':

    dbConnector = MSGDBConnector()
    cursor = dbConnector.conn.cursor()
    weatherUtil = MSGWeatherDataUtil()

    msg = "Downloading NOAA weather data."
    print msg
    MSG_BODY = '%s\n' % msg

    msg = "Last loaded date is %s." % weatherUtil.datePart(
        datetime = weatherUtil.getLastDateLoaded(cursor))
    print msg
    MSG_BODY += '%s\n' % msg

    retriever = MSGWeatherDataRetriever()
    configer = MSGConfiger()
    WEATHER_DATA_PATH = configer.configOptionValue('Weather Data',
                                                   'weather_data_path')

    msg = "Using URL %s." % weatherDataURL
    print msg
    MSG_BODY += '%s\n' % msg

    msg = "Using pattern %s." % weatherDataPattern
    print msg
    MSG_BODY += '%s\n' % msg

    global logger
    logger = MSGLogger(__name__)
    weatherDataURL = configer.configOptionValue('Weather Data',
                                                'weather_data_url')

    retriever.fileList = retriever.weatherUtil.fileList
    retriever.dateList = retriever.weatherUtil.dateList

    multiprocessingLimit = configer.configOptionValue('Hardware',
                                                      'multiprocessing_limit')

    if retriever.fileList:
        msg = "Performing primary retrieval."
        print msg
        MSG_BODY += '%s\n' % msg

        retriever.pool = multiprocessing.Pool(int(multiprocessingLimit))
        results = retriever.pool.map(performDownloading, retriever.fileList)
        retriever.pool.close()
        retriever.pool.join()

        if False in results:
            msg = "An error occurred during primary retrieval."
            print msg
            MSG_BODY += '%s\n' % msg


    # Force download on intermediate dates between last loaded date and now.
    # If a date is less than the last loaded date, remove it from the list,
    # effectively.

    # Get the keep list.
    keepList = weatherUtil.getKeepList(retriever.fileList, cursor)
    if keepList:
        msg = "Performing secondary retrieval."
        print msg
        MSG_BODY += '%s\n' % msg

        retriever.pool = multiprocessing.Pool(int(multiprocessingLimit))
        results = retriever.pool.map(performDownloadingWithForcedDownload,
                                     keepList)
        retriever.pool.close()
        retriever.pool.join()

        if False in results:
            msg = "An error occurred during secondary retrieval."
            print msg
            MSG_BODY += '%s\n' % msg


    # Just retrieve the last set if nothing else was retrieved.
    if downloadCount == 0:
        # Retrieve last dated set if nothing else was retrieved.
        retriever.dateList.sort()
        performDownloading(retriever.fileList[-1], forceDownload = True)

    msg = "downloadCount = %s." % downloadCount
    print msg
    MSG_BODY += '%s\n' % msg

    cleanUpTxtFiles()
    saveRetrievalResults()
