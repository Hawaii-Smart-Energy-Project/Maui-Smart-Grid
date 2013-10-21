#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

Generates random unit testing data for the MSG eGauge Service.

The format is a date and time column containing a Unix timestamp followed by
energy reading columns that consist of signed floating point values.

"""

__author__ = 'Daniel Zhang (張道博)'
__copyright__ = 'Copyright (c) 2013, University of Hawaii Smart Energy Project'
__license__ = 'https://raw.github' \
              '.com/Hawaii-Smart-Energy-Project/Maui-Smart-Grid/master/BSD' \
              '-LICENSE.txt'

import random
import datetime
import calendar

headerCols = ["Date & Time", "AC [kW]", "AC+ [kW]", "Addition [kW", "DHW [kW]",
              "Dishwasher [kW]", "Dryer [kW]", "Dryer.Usage [kW]", "Fan [kW]",
              "Garage AC [kW]", "Garage AC.Usage [kW]", "gen [kW]", "Grid [kW]",
              "House [kW]", "Large AC [kW]", "Large AC.Usage [kW]", "Oven [kW]",
              "Oven and Microwave [kW]", "Oven and Microwave+ [kW]",
              "Oven.Usage [kW]", "Range [kW]", "Range.Usage [kW]",
              "Refrigerator [kW]", "Refrigerator.Usage [kW]",
              "Rest of House.Usage [kW]", "Shop [kW]", "Solar [kW]",
              "Solar Pump [kW]", "Stove [kW]", "Stove Top [kW]", "use [kW]",
              "Washer [kW]", "Washer.Usage [kW]", "Whole House [kW]"]

rows = range(1000)

startTime = datetime.datetime.now()

for c in headerCols:
    print c

for i in rows:
    for c in headerCols:
        if c == "Date & Time":
            unixTime = calendar.timegm(startTime.utctimetuple()) + i
            print unixTime,
        else:
            signValue = -1 if random.random() < 0.5 else 1
            print random.random() * 240.0 * signValue,

        if headerCols.index(c) == len(headerCols) - 1:
            print
