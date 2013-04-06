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
                Testing_MeterData
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

my $dumpCommand = "pg_dump -t '\"%s\"' -s -h $hostname $databaseName > %s/%s.sql";
my $dest;

$dest = "tables";
if(!-d $dest){ mkdir $dest; }

foreach my $t (@tables) {
    print "Dumping table $t\n";
    my $result = system(sprintf($dumpCommand,$t,$dest,$t));

    if ($result != 0) {
        removeFailedDump($dest,$t);
    }
}

$dest = "views";
if(!-d $dest){ mkdir $dest; }

foreach my $v (@views) {
    print "Dumping view $v\n";
    my $result = system(sprintf($dumpCommand,$v,$dest,$v));

    if ($result != 0) {
        removeFailedDump($dest,$v);
    }
}

sub removeFailedDump
{
    my ($path, $file) = @_;
    print "removing failed dump.\n";
    my $rmResult = system("rm $path/$file.sql");
}
