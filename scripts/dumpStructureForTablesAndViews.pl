#!/usr/bin/env perl

# Dump structure of MECO database tables, and views, so they can be recreated
# in another database.
#
# Usage:
#
#   perl dumpStructureForTables.pl ${HOSTNAME} ${DATABASE_NAME}
#
# @author Daniel Zhang (張道博)

use strict;

print "Dumping table structure for MECO database.\n";

my $hostname = $ARGV[0];
my $databaseName = $ARGV[1];

if (!$hostname || !$databaseName) {
    print "\nUsage: perl dumpStructureForTables.pl \${HOSTNAME} \${DATABASE_NAME}\n";
    exit;
}

my @tables = qw(Interval
                IntervalReadData
                LocationRecords
                MeterData
                MeterRecords
                Reading
                Register
                RegisterData
                RegisterRead
                TestMeterData
                Tier
                WeatherData
                WeatherKahaluiAirport
                );

my @views = qw(Distinct_kWh_3channels_and_location
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

my $dumpCommand = "pg_dump -t '\"$t\"' -s -h $hostname $databaseName > $t.sql";

foreach my $t (@tables) {
    print "Dumping table $t\n";
    my $result = system($dumpCommand);

    # remove failed dump
    if ($result != 0) {
        my $rmResult = system("rm $t.sql");
    }
}

foreach my $v (@views) {
    print "Dumping view $v\n";
    my $result = system($dumpCommand);

    # remove failed dump
    if ($result != 0) {
        my $rmResult = system("rm $v.sql");
    }
}
