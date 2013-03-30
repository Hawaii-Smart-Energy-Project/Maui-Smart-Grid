#!/usr/bin/env perl

# Dump structure of MECO database tables.
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
               );

foreach my $t (@tables) {
    print "Dumping table $t\n";
    my $result = system("pg_dump -t '\"$t\"' -s -h $hostname $databaseName > $t.sql");

    # remove failed dump
    if ($result != 0) {
        my $rmResult = system("rm $t.sql");
    }
}
