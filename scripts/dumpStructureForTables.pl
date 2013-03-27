#!/usr/bin/env perl

# Dump structure of MECO database tables.
#
# Usage:
#
#   perl dumpStructureForTables.pl ${DATABASE_NAME} ${HOSTNAME}
#
# @author Daniel Zhang (張道博)

use strict;

print "Dumping table structure for MECO database.\n";

my $hostname = $ARGV[1];
my $databaseName = $ARGV[0];

if (!$hostname || !$databaseName) {
    print "\nUsage: perl dumpStructureForTables.pl \${DATABASE_NAME} \${HOSTNAME}\n";
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
               );

foreach my $t (@tables) {
    print "Dumping table $t\n";
    my $result = system("pg_dump -t '\"$t\"' -s $databaseName -h $hostname > $t.sql");
}
