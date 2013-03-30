#!/usr/bin/env perl

# Add MECO tables to an existing database.
#
# Usage:
#
#   perl addTablesToDatabase.pl ${HOSTNAME} ${DATABASE_NAME}
#
# PostgreSQL password should be set in ~/.pgpass with the format:
#
#   hostname:port:database:username:password
#
# where individual fields can be substituted with a wildcard indicated by '*'.
#
# @author Daniel Zhang (張道博)

use strict;

my @tables = qw (MeterData
                 IntervalReadData
                 Interval
                 Reading
                 RegisterData
                 RegisterRead
                 Tier
                 Register
                 MeterRecords
                 LocationRecords
                 WeatherData
                );

my $hostname = $ARGV[0];
my $databaseName = $ARGV[1];

if (!$hostname || !$databaseName) {
    print "\nUsage: perl addTablesToDatabase.pl \${HOSTNAME} \${DATABASE_NAME}\n";
    exit;
}

print "Adding tables to database $databaseName.\n";

if (!$hostname || !$databaseName) {
    print "\nUsage: perl addTablesToDatabase.pl \${HOSTNAME} \${DATABASE_NAME}\n";
    exit;
}

my $result;
foreach my $t (@tables) {
    $result = system("psql -w -h $hostname $databaseName < $t.sql");
}

