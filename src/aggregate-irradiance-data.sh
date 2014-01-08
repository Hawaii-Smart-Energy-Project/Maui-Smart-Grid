#!/bin/bash

# Generate aggregated irradiance data in half-year portions.
#
# Usage:
#
#   aggregate-irradiance-data.sh
#
# @author Daniel Zhang (張道博)

time python aggregateIrradianceData.py --startDate "2012-01-01 00:00:00" --endDate "2012-06-30 11:45:00" > avg-irradiance-15-min-2012-first-half.csv
time python aggregateIrradianceData.py --startDate "2012-06-30 11:45:00" --endDate "2013-01-01 00:00:00" > avg-irradiance-15-min-2012-second-half.csv
time python aggregateIrradianceData.py --startDate "2013-01-01 00:00:00" --endDate "2013-06-30 11:59:59" > avg-irradiance-15-min-2013-first-half.csv
time python aggregateIrradianceData.py --startDate "2013-06-30 11:45:00" --endDate "2014-01-01 00:00:00" > avg-irradiance-15-min-2013-second-half.csv
time python aggregateIrradianceData.py --startDate "2014-01-01 00:00:00" --endDate "2014-06-30 11:59:59" > avg-irradiance-15-min-2014-first-half.csv
