# MECO Perl support library.
#
# @author Daniel Zhang (張道博)
#
# Using this module may require adding its location to the PERL5LIB env variable.
#
# This module contains data structures for tables and views, both past and present.

package MECOLib;
use strict;
use warnings;

require Exporter;
our @ISA       = qw(Exporter);
our @EXPORT_OK = qw(@tables @views);

our @tables = qw(MeterData
                 RegisterData
                 RegisterRead
                 Tier
                 Register
                 IntervalReadData
                 Interval
                 Reading
                 LocationRecords
                 MeterRecords
                 Testing_MeterData
                 WeatherKahaluiAirport
                );

our @views = qw(Distinct_kWh_3channels_and_location
                Distinct_Voltage_and_Location
                get_kwh_meter_locations
                get_meter_readings_locations
                get_voltage_with_interval
                get_voltage_with_meter_id
                get_voltages
                meter_locations
                meter_V_readings_and_locations
                viewReadings
               );
