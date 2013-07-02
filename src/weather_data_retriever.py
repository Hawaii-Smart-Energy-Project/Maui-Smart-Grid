#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'

import urllib2
import re
import pycurl
from mecoconfig import MECOConfiger
from mecologger import MECOLogger


class WeatherDataRetriever(object):
    """
    Retrieve NOAA weather data relevant to the MSG project.
    """

    def __init__(self):
        self.logger = MECOLogger(__name__, 'info')
        self.configer = MECOConfiger()
        self.weatherDataPath = self.configer.configOptionValue('Weather Data',
                                                               'weather_data_path')

    def downloadWeatherData(self):
        url = "http://cdo.ncdc.noaa.gov/qclcd_ascii/"
        pattern = '<A HREF=".*?">(QCLCD(2012|2013).*?)</A>'

        response = urllib2.urlopen(url).read()

        for filename in re.findall(pattern, response):
            print filename[0]
            fp = open(self.weatherDataPath + "/" + filename[0], "wb")
            curl = pycurl.Curl()
            curl.setopt(pycurl.URL, url + "/" + filename[0])
            curl.setopt(pycurl.WRITEDATA, fp)
            curl.perform()
            curl.close()
            fp.close()


retriever = WeatherDataRetriever()
retriever.downloadWeatherData()


