#!/usr/bin/perl -w

# Installation script for
# eGauge Automatic Data Services
#
# @author Daniel Zhang (張道博)
# @copyright Copyright (c) 2013, University of Hawaii Smart Energy Project
# @license https://raw.github.com/Hawaii-Smart-Energy-Project/Maui-Smart-Grid/master/BSD-LICENSE.txt
#
# Usage:
#
#     sudo ./installEgaugeAutomaticDataServices.pl

use strict;

my $installRoot = "/usr/local/msg-egauge-service";
my $binDest     = "/usr/local/msg-egauge-service/bin";
my $libDest     = "/usr/local/lib/perl5";
my $configDest  = "/usr/local/msg-egauge-service/config";

if ( !-e $installRoot && !-d $installRoot ) {
    print "Making root directory at $installRoot.\n";
    mkdir($installRoot);
}

if ( !-e $binDest && !-d $binDest ) {
    print "Making bin directory at $binDest.\n";
    mkdir($binDest);
}

if ( !-e $libDest && !-d $libDest ) {
    print "Making lib directory at $libDest.\n";
    mkdir($libDest);
}

if ( !-e $configDest && !-d $configDest ) {
    print "Making config directory at $configDest.\n";
    mkdir($configDest);
}

if (   ( !-e $installRoot && !-d $installRoot )
    || ( !-e $binDest    && !-d $binDest )
    || ( !-e $libDest    && !-d $libDest )
    || ( !-e $configDest && !-d $configDest ) )
{
    print "ERROR: Not all install paths exist.\n";
    exit;
}

print "Copying files...\n";

`cp getEgaugeData.pl $binDest`;
`cp insertEgaugeData.pl $binDest`;
`cp DZSEPLib.pm $libDest`;

print "Finished.\n";

