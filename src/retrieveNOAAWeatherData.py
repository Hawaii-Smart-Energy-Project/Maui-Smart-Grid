#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

Parallelized weather retrieval and processing.

@todo Convert fully to class versus the current hybrid implementation.

"""

__author__ = 'Daniel Zhang (張道博)'

import urllib2
import re
import pycurl
from msg_config import MSGConfiger
from msg_logger import MSGLogger
import multiprocessing
import zipfile
import os.path
import os
import gzip
from msg_weather_data_util import MSGWeatherDataUtil

weatherDataPath = ''
retriever = None
logger = MSGLogger(__name__, 'info')
downloadCount = 0


class MSGWeatherDataRetriever(object):
    """
    Retrieve national NOAA weather data relevant to the MSG project and save it
    to local storage in the path given in the configuration file for [Weather
     Data], weather_data_path.

    Unzip the retrieved data and recompress the hourly data using gzip.
    """

    def __init__(self):
        self.logger = MSGLogger(__name__, 'info')
        self.configer = MSGConfiger()
        self.weatherDataPath = self.configer.configOptionValue('Weather Data',
                                                               'weather_data_path')
        self.queue = multiprocessing.JoinableQueue()
        self.procs = []
        self.pool = None
        self.fileList = []
        self.dateList = []
        self.weatherUtil = MSGWeatherDataUtil()

        global weatherDataPath
        weatherDataPath = self.configer.configOptionValue('Weather Data',
                                                          'weather_data_path')

    # def fillFileList(self):
    #
    #     url = "http://cdo.ncdc.noaa.gov/qclcd_ascii/"
    #     pattern = '<A HREF=".*?">(QCLCD(' \
    #               '201208|201209|201210|201211|201212|2013).*?)</A>'
    #     response = urllib2.urlopen(url).read()
    #
    #     for filename in re.findall(pattern, response):
    #         self.fileList.append(filename[0])
    #         self.dateList.append(datePart(filename[0]))


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


# def datePart(filename):
#     newName = filename.replace("QCLCD", '')
#     newName = newName.replace(".zip", '')
#     return newName


def unzipWorker(filename, forceDownload = False):
    originalName = filename

    global retriever
    hourlyGzName = retriever.weatherUtil.datePart(filename) + "hourly.txt.gz"
    if fileExists(hourlyGzName) and not forceDownload:
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
                originalName) + "hourly.txt"

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
    if not fileExists(filename) or forceDownload:
        global weatherDataPath
        url = "http://cdo.ncdc.noaa.gov/qclcd_ascii/"
        print "Performing download on " + filename
        fp = open(weatherDataPath + "/" + filename, "wb")
        curl = pycurl.Curl()
        curl.setopt(pycurl.URL, url + "/" + filename)
        curl.setopt(pycurl.WRITEDATA, fp)
        curl.perform()
        curl.close()
        fp.close()

    if fileExists(filename) or forceDownload:
        unzipFile(filename, forceDownload)

    global downloadCount
    downloadCount += 1


if __name__ == '__main__':
    retriever = MSGWeatherDataRetriever()


    # retriever.fillFileList()
    retriever.fileList = retriever.weatherUtil.fileList
    retriever.dateList = retriever.weatherUtil.dateList

    retriever.pool = multiprocessing.Pool(4)
    retriever.pool.map(performDownloading, retriever.fileList)
    retriever.pool.close()
    retriever.pool.join()

    if downloadCount == 0:
        # Retrieve last dated set if all others are present.
        retriever.dateList.sort()
        performDownloading(retriever.fileList[-1], forceDownload = True)

