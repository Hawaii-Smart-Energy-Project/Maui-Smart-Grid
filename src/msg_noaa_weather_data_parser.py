#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'

import csv
import re


class MSGNOAAWeatherDataParser(object):
    """
    Given a file object containing NOAA weather data, return a data structure
     containing the data.
    """

    def __init__(self):
        """
        Constructor.
        """
        pass


    def parseWeatherData(self, fileObject, stationIDs):
        """
        :param fileObject: File object containing weather data.
        :param stationIDs: List of station IDs to be parsed.
        :returns: List of lists containing parsed weather data.
        """
        rowNum = 0
        lastCol = 0

        reader = csv.reader(fileObject)
        self.data = []

        for row in reader:
            rowData = []
            newDate = ''

            # Handle the header row.
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
                            pass
                        else:
                            # Skip station IDs not marked for processing.
                            break

                    elif colNum == 1: # date column
                        newDate = '%s' % (
                            (col[0:4]) + '-%s' % (col[4:6]) + '-%s' % (
                                col[6:8]))

                    elif colNum == 2: # time column
                        time = col.zfill(4)
                        rowData.append(
                            '%s %s:%s' % (newDate, time[0:2], time[2:4]))
                        newDate = ''
                    else:
                        rowData.append('%s' % col)
                    colNum += 1

                    if colNum == lastCol:
                        for i in range(0, lastCol - 1):

                            try:
                                if len(rowData[i]) == 0 or len(
                                        re.sub("\s+", "", rowData[i])) == 0:
                                    rowData[i] = 'NULL'
                                else:
                                    rowData[i] = "'" + rowData[i] + "'"
                            except IndexError, e:
                                assert rowData != [], "Data should never be " \
                                                      "empty."

                        self.data.append(rowData)
                        # End for col

            rowNum += 1

        # End for row

        # print self.data
        return self.data


    def stationShouldBeProcessed(self, myStationID, stationIDs = []):
        """
        :param myStationID: Station ID to be tested.
        :param stationIDs: List of station IDs.
        :returns: True if a station ID is in the list of station IDs to be
        processed.
        """
        for sid in stationIDs:
            if myStationID == sid:
                return True
        return False
        pass
