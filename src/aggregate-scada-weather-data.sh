#!/bin/bash

# @DEPRECATED in favor of MSGDataAggregator.
#
# Generate aggregated SCADA weather data (temperature/humidity).
#
# Usage:
#
#   aggregate-scada-weather-data.sh
#
# @author Daniel Zhang (張道博)

time python aggregateSCADAWeatherData.py --startDate "2013-07-01 00:00:00" --endDate "2014-06-01 00:00:00" > avg-scada-weather-data.csv
