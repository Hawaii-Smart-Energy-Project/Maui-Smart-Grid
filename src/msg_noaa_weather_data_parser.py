#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'
__copyright__ = 'Copyright (c) 2013, University of Hawaii Smart Energy Project'
__license__ = 'https://raw.github' \
              '.com/Hawaii-Smart-Energy-Project/Maui-Smart-Grid/master/BSD' \
              '-LICENSE.txt'

import csv
import re
from sek.logger import SEKLogger


class MSGNOAAWeatherDataParser(object):
    """
    Given a file object containing NOAA weather data, return a data structure
    containing the data.
    """

    def __init__(self):
        """
        Constructor.
        """
        self.logger = SEKLogger(__name__, 'debug')

        self.cols = ["wban", "datetime", "datetime", "station_type",
                     "sky_condition", "sky_condition_flag", "visibility",
                     "visibility_flag", "weather_type", "weather_type_flag",
                     "dry_bulb_farenheit", "dry_bulb_farenheit_flag",
                     "dry_bulb_celsius", "dry_bulb_celsius_flag",
                     "wet_bulb_farenheit", "wet_bulb_farenheit_flag",
                     "wet_bulb_celsius", "wet_bulb_celsius_flag",
                     "dew_point_farenheit", "dew_point_farenheit_flag",
                     "dew_point_celsius", "dew_point_celsius_flag",
                     "relative_humidity", "relative_humidity_flag",
                     "wind_speed", "wind_speed_flag", "wind_direction",
                     "wind_direction_flag", "value_for_wind_character",
                     "value_for_wind_character_flag", "station_pressure",
                     "station_pressure_flag", "pressure_tendency",
                     "pressure_tendency_flag", "pressure_change",
                     "pressure_change_flag", "sea_level_pressure",
                     "sea_level_pressure_flag", "record_type",
                     "record_type_flag", "hourly_precip", "hourly_precip_flag",
                     "altimeter", "altimeter_flag"]

    def parseWeatherData(self, fileObject, stationIDs):
        """
        :param fileObject: File object containing weather data.
        :param stationIDs: List of station IDs to be parsed.
        :returns: List of dictionaries containing parsed weather data.
        """
        self.logger.log('Data column count = %s' % len(self.cols), 'debug')

        rowNum = 0
        lastCol = 0

        reader = csv.reader(fileObject)
        self.data = []

        for row in reader:
            rowDict = {}

            newDate = ''

            # Handle the header row and determine the last column.
            if rowNum == 0:
                colNum = 0
                for col in row:
                    colNum += 1
                lastCol = colNum

            else:
                colNum = 0

                for col in row:

                    if colNum == 0:
                        if self.stationShouldBeProcessed(col, stationIDs):
                            rowDict['wban'] = col
                        else:
                            # Skip station IDs not marked for processing.
                            break

                    elif colNum == 1: # date column
                        newDate = '%s' % (
                            (col[0:4]) + '-%s' % (col[4:6]) + '-%s' % (
                                col[6:8]))

                    elif colNum == 2: # time column
                        time = col.zfill(4)
                        rowDict['datetime'] = '%s %s:%s' % (
                            newDate, time[0:2], time[2:4])
                        newDate = ''
                    else:
                        try:
                            rowDict[self.cols[colNum]] = '%s' % col
                        except IndexError, e:
                            print "Exception during first assignment: %s, " \
                                  "Index = %s" % (
                                      e, colNum)
                    colNum += 1

                    if colNum == lastCol:
                        for i in range(0, lastCol - 1):

                            try:
                                if len(rowDict[self.cols[i]]) == 0 or len(
                                        re.sub("\s+", "",
                                               rowDict[self.cols[i]])) == 0:
                                    rowDict[self.cols[i]] = 'NULL'

                            except IndexError, e:
                                print "Exception during second assignment: " \
                                      "%s, Index = %s" % (
                                          e, i)

                        assert rowDict != {}, "Dict should never be empty."

                        self.data.append(rowDict)

                        # End for col

            rowNum += 1

            # End for row

        return self.data


    def stationShouldBeProcessed(self, myStationID, stationIDs = None):
        """
        :param myStationID: Station ID to be tested.
        :param stationIDs: List of station IDs.
        :returns: True if a station ID is in the list of station IDs to be
        processed.
        """

        if stationIDs is None:
            stationIDs = []
        for sid in stationIDs:
            if myStationID == sid:
                return True
        return False
        pass
