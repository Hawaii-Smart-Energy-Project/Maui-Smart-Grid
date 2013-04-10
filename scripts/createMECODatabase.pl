#!/usr/bin/env perl

# Create a MECO database from SQL files dumped by pg_dump.
# This script runs the necessary commands to create a MECO database.
#
# Usage:
#
# createMECODatabase.pl ${DATABASE_NAME}
#
# @author Daniel Zhang (張道博)

use strict;
use MECOLib;

if (!$ARGV[0]) {
    print "Usage: createMECODatabase.pl \${DATABASE_NAME}\n";
    exit(0);
}

if (!-e "tables" || !-e "views") {
    print "Both tables and views need to be present.\n";
    exit(0);
}

my $db = $ARGV[0];

foreach my $table (@MECOLib::tables) {
    my $cmd = sprintf("sudo -u postgres psql %s < tables/%s.sql", $db, $table);
    print "$cmd\n";
    `$cmd`;
}
foreach my $view (@MECOLib::views) {
    my $cmd = sprintf("sudo -u postgres psql %s < views/%s.sql", $db, $view);
    print "$cmd\n";
    `$cmd`;
}
