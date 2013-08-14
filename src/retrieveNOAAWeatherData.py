#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

Parallelized weather retrieval and processing.

@todo Convert fully to class versus the current hybrid implementation.

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
        try:
            with open(filename):
                return True

        except IOError, e:
            # self.logger.log("IO Error: %s" % e, 'error')
            return False

        return False

# ********** End Class **********

def fileExists(filename):
    try:
        with open(filename):
            return True

    except IOError, e:
        logger.log("%s" % e, 'info')
        return False

    return False


def unzipWorker(filename, forceDownload = False):
    originalName = filename

    hourlyGzName = retriever.weatherUtil.datePart(
        filename = filename) + "hourly.txt.gz"
    if fileExists(hourlyGzName) and not forceDownload:
        print "%s already exists." % hourlyGzName
        return

    if (fileExists(filename)):
        print "Unzipping %s." % filename
        try:

            zfile = zipfile.ZipFile(filename)
            for name in zfile.namelist():
                (dirname, filename) = os.path.split(name)
                if not dirname == '':
                    print "Decompressing " + filename + " into " + dirname + "."
                else:
                    print "Decompressing " + filename + "."
                if not os.path.exists(dirname) and not dirname == '':
                    os.mkdir(dirname)
                fd = open(name, "w")
                fd.write(zfile.read(name))
                fd.close()

            hourlyName = retriever.weatherUtil.datePart(
                filename = originalName) + "hourly.txt"

            if fileExists(hourlyName):
                print "Hourly file exists"
                gzipCompressFile(hourlyName)
            else:
                print "Hourly file not found."
        except zipfile.BadZipfile:
            print "Bad zipfile %s." % originalName
            pass


def gzipCompressFile(filename):
    f_in = open(filename, 'rb')
    f_out = gzip.open(filename + ".gz", 'wb')
    f_out.writelines(f_in)
    f_out.close()
    f_in.close()


def unzipFile(filename, forceDownload = False):
    unzipWorker(filename, forceDownload)


def performDownloading(filename, forceDownload = False):
    logger.log('')

    success = True
    if not fileExists(filename) or forceDownload:
        print "Performing download on " + filename
        fp = open(weatherDataPath + "/" + filename, "wb")
        curl = pycurl.Curl()
        curl.setopt(pycurl.URL, weatherDataURL + "/" + filename)
        curl.setopt(pycurl.WRITEDATA, fp)
        try:
            curl.perform()
        except pycurl.error, e:
            errorCode, errorText = e.args
            logger.log('Error during retrieval: code: %s, text: %s.' % (
                errorCode, errorText))
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
    Clean up unused txt files.
    """

    patterns = ['*hourly.txt', '*daily.txt', '*monthly.txt', '*precip.txt',
                '*remarks.txt', '*station.txt']
    for root, dirs, filenames in os.walk(
            configer.configOptionValue('Weather Data', 'weather_data_path')):
        for pat in patterns:
            for filename in fnmatch.filter(filenames, pat):
                os.remove(filename)
                print "Removed %s." % filename


if __name__ == '__main__':
    dbConnector = MSGDBConnector()
    cursor = dbConnector.conn.cursor()
    weatherUtil = MSGWeatherDataUtil()

    print "Downloading NOAA weather data."
    print "Last loaded date is %s." % weatherUtil.datePart(
        datetime = weatherUtil.getLastDateLoaded(cursor))

    retriever = MSGWeatherDataRetriever()
    configer = MSGConfiger()

    print "Using URL %s." % weatherDataURL
    print "Using pattern %s." % weatherDataPattern

    global logger
    logger = MSGLogger(__name__)
    weatherDataURL = configer.configOptionValue('Weather Data',
                                                'weather_data_url')

    retriever.fileList = retriever.weatherUtil.fileList
    retriever.dateList = retriever.weatherUtil.dateList

    LAST_DATE_TESTING = False
    if not LAST_DATE_TESTING:
        if retriever.fileList:
            print "Performing primary retrieval."

            retriever.pool = multiprocessing.Pool(4)
            results = retriever.pool.map(performDownloading, retriever.fileList)
            retriever.pool.close()
            retriever.pool.join()

            if False in results:
                print "An error occurred during primary retrieval."
                # print results

    # Force download on intermediate dates between last loaded date and now.
    # If a date is less than the last loaded date, remove it from the list,
    # effectively.

    # Get the keep list.
    keepList = weatherUtil.getKeepList(retriever.fileList, cursor)
    if keepList:
        print "Performing secondary retrieval."

        retriever.pool = multiprocessing.Pool(4)
        results = retriever.pool.map(performDownloadingWithForcedDownload,
                                     keepList)
        retriever.pool.close()
        retriever.pool.join()

        if False in results:
            print "An error occurred during secondary retrieval."


    # Just retrieve the last set if nothing else was retrieved.
    if downloadCount == 0:
        # Retrieve last dated set if nothing else was retrieved.
        retriever.dateList.sort()
        performDownloading(retriever.fileList[-1], forceDownload = True)

    print "downloadCount = %s." % downloadCount
    cleanUpTxtFiles()
