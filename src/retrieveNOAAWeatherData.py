#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Retrieve NOAA weather data to local storage.
"""

__author__ = 'Daniel Zhang (張道博)'

from msg_weather_data_retriever import MSGWeatherDataRetriever
import argparse


def processCommandLineArguments():
    global parser, commandLineArgs
    parser = argparse.ArgumentParser(
        description = 'Retrieve NOAA hourly weather data to local storage.')
    parser.add_argument('--email', action = 'store_true', default = False,
                        help = 'Send email notification if this flag is '
                               'specified.')
    parser.add_argument('--testing', action = 'store_true', default = False,
                        help = '')
    commandLineArgs = parser.parse_args()


processCommandLineArguments()
retriever = MSGWeatherDataRetriever()
retriever.downloadWeatherData()
