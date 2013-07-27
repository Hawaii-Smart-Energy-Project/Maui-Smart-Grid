#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'

import urllib2
import re

class MSGWeatherDataUtil(object):
    """
    Utility methods for working with weather data.
    """

    def __init__(self):
        """
        Constructor.
        """

        self.url = "http://cdo.ncdc.noaa.gov/qclcd_ascii/"
        self.pattern = '<A HREF=".*?">(QCLCD(201208|201209|201210|201211|201212|2013).*?)</A>'
        self.fileList = []
        self.dateList = []
        self.fillFileListAndDateList()

    def fillFileListAndDateList(self):
        """
        Return a list of weather files used in processing weather data.
        """

        response = urllib2.urlopen(self.url).read()

        for filename in re.findall(self.pattern, response):
            self.fileList.append(filename[0])
            self.dateList.append(self.datePart(filename[0]))


    def datePart(self, filename):
        newName = filename.replace("QCLCD", '')
        newName = newName.replace(".zip", '')
        return newName
