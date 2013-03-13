#!/usr/bin/env perl

# Create a fresh MECO database.
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
                );

my $database = "test_meco";

foreach my $t (@tables) {
    `sudo -u postgres psql $database < $t.sql`;
}

