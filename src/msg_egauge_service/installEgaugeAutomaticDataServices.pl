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
# sudo ./installEgaugeAutomaticDataServices.pl

use strict;

# @todo Make directories if they don't already exist.

my $binDest = "/usr/local/msg-egauge-service/bin";
my $libDest = "/usr/local/lib/perl5";
my $configDest = "/usr/local/msg-egauge-service/config";

`cp getEgaugeData.pl $binDest`;
`cp insertEgaugeData.pl $binDest`;
`cp DZSEPLib.pm $libDest`;
