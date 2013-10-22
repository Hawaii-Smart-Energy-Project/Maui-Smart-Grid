#!/usr/bin/perl -w

# Installation script for MSG eGauge Automatic Data Services
#
# @author Daniel Zhang (張道博)
#
# @copyright Copyright (c) 2013, University of Hawaii Smart Energy Project
# @license https://raw.github.com/Hawaii-Smart-Energy-Project/Maui-Smart-Grid/master/BSD-LICENSE.txt
#
# Usage:
#
#     sudo perl installEgaugeAutomaticDataServices.pl

use strict;
use Cwd qw(abs_path getcwd);
use File::Basename;

my $sourcePath  = dirname( abs_path($0) );
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

print "Installing from $sourcePath.\n";

chdir($sourcePath) or die "Cannot change to $sourcePath.\n";

print "Copying files...\n\n";

my $cmd;

my @cmds = (
    "cp getEgaugeData.pl $binDest",
    "cp insertEgaugeData.pl $binDest",
    "cp DZSEPLib.pm $libDest"
);

foreach (@cmds) {
    print "$_\n";
    `$_`;
}

print "\nFinished.\n";

