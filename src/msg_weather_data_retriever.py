#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'

import urllib2
import re
import pycurl
from msg_config import MSGConfiger
from msg_logger import MSGLogger


class MSGWeatherDataRetriever(object):
    """
    Retrieve national NOAA weather data relevant to the MSG project and save it
    to local storage in the path given in the configuration file for [Weather
     Data], weather_data_path.
    """

    def __init__(self):
        self.logger = MSGLogger(__name__, 'info')
        self.configer = MSGConfiger()
        self.weatherDataPath = self.configer.configOptionValue('Weather Data',
                                                               'weather_data_path')

    def downloadWeatherData(self):
        url = "http://cdo.ncdc.noaa.gov/qclcd_ascii/"
        pattern = '<A HREF=".*?">(QCLCD(' \
                  '201208|201209|201210|201211|201212|2013).*?)</A>'

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
