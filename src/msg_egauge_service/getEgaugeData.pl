#!/usr/bin/perl

###
# Retrieve all data for all eGauges in CSV format.
# Retrieve data from the last date recorded in the database by each house.
#
# If there is a power loss or reboot during data retrieval, the data may not be complete.
# Invalid data is saved in a separate directory.
#
# @author Daniel Zhang (張道博)
# @copyright Copyright (c) 2013, University of Hawaii Smart Energy Project
# @license https://raw.github.com/Hawaii-Smart-Energy-Project/Maui-Smart-Grid/master/BSD-LICENSE.txt
##

use strict;
use DZSEPLib;
use Config::General;

my $conf
    = new Config::General(
    "/usr/local/msg-egauge-service/config/egauge-automatic-data-services.config"
    );
if ( !$conf ) { die "ERROR: Invalid config" }
my %CONFIG = $conf->getall;

my $FOUND_INVALID_DATA = 0;

my @egauges = @{ $CONFIG{egauge} };

my $dataDir = $CONFIG{data_dir};    # Root location for data downloads.

if ( chdir($dataDir) ) {
    print "Changed to $dataDir.\n";
}
else {
    print "Can't change to data directory.\n";
    exit;
}

DZSEPLib::connectDatabase(
    $CONFIG{fc_dbname}, $CONFIG{db_host}, $CONFIG{db_port},
    $CONFIG{db_user},   $CONFIG{db_pass}
);

#my $houseMappingRef = DZSEPLib::mapEgaugeNumbersToHouseID();
my $dataDirName     = DZSEPLib::getDateString();

print "New data will be added to $dataDirName.\n";

if ( mkdir($dataDirName) ) {
    if ( -d $dataDirName ) {
        print "$dataDirName created successfully.\n";
    }
    else {
        print "Directory $dataDirName was not created.\n";
        exit;
    }
}

if ( chdir($dataDirName) ) {
    print "Changing directory to $dataDirName.\n";
}
else {
    print "Can't change to directory $dataDirName.\n";
    exit;
}

# Options:
#     m = n & s parameters are specified in minutes
#     c = return output in CSV format
#     C = return delta compressed data
#     w = return data only new than the timestamp
foreach my $g (@egauges) {

    #$house = "egauge" . $house;
    
    print "\tRetrieving data for eGauge $g.\n";

    my $filename = lc($g) . ".csv";

    #my $egaugeNumber = $house;
    #my $houseNumber  = 0;
    
    # @todo eliminate redundant use of egauge number
    if ( $g =~ /(\d+)$/ ) {
        $g = $1;
        print STDERR "\tegauge number = $g\n";
    }

    #if ( $houseMappingRef->{$egaugeNumber} ) {
        #$houseNumber = $houseMappingRef->{$egaugeNumber};
    #}

    #print STDERR "\thouse number = $houseNumber\n";

    my $lastUnixTimestamp
        = DZSEPLib::getLastUnixTimestampForMSGEnergyAutoloadGauge($g);
    print STDERR "last datetime = $lastUnixTimestamp\n";

    my $retrieveCommand
        = sprintf(
        "wget \"http://%s.egaug.es/cgi-bin/egauge-show?m&c&C&w=$lastUnixTimestamp\" -O $filename",
        lc($g) );
    print "\tcommand=$retrieveCommand\n";
    `$retrieveCommand`;

    if ( DZSEPLib::verifyData($filename) != 1 ) {
        print "\tInvalid data for $filename...\n";
        $FOUND_INVALID_DATA = 1;
        last;
    }
}

# Move invalid data to the invalid data directory and exit with an error.
if ( $FOUND_INVALID_DATA == 1 ) {
    if ( chdir($dataDir) ) {
        print "\tChanged to $dataDir.\n";
    }
    else {
        die "Can't change to data directory.\n";
    }

    print "\tmoving $dataDirName to ";
    print $CONFIG{invalid_data_dir};
    print "\n";
    DZSEPLib::moveReliable( $dataDirName, $CONFIG{invalid_data_dir} );
    exit(-1);
}

exit(0);
