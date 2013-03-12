#!/usr/bin/env perl

# Dump structure of MECO database tables.
#
# @author Daniel Zhang (張道博)

use strict;

print "Dumping table structure for MECO database.\n";

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
    `pg_dump -t '"$t"' -s meco > $t.sql`
}
