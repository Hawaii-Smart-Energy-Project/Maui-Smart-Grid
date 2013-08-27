#!/usr/bin/perl

###
# Insert eGauge energy data into the database
#
# House IDs are obtained from hash egMap.
# Header column mappings to SQL columns are obtained through hash colAssoc.
#
# The existence of dupes are checked before loading so that no duplicate record insertions are ever attempted.
#
# @author Daniel Zhang (張道博)
# @copyright Copyright (c) 2013, University of Hawaii Smart Energy Project
# @license https://raw.github.com/Hawaii-Smart-Energy-Project/Maui-Smart-Grid/master/BSD-LICENSE.txt
##

use strict;
use warnings;
use DBI;
use Getopt::Long;
use DZSEPLib;
use Config::General;
use File::Basename;

my $conf
    = new Config::General(
    "/usr/local/msg-egauge-service/config/egauge-automatic-data-services.config"
    );
if ( !$conf ) { die "ERROR: Invalid config" }
my %CONFIG = $conf->getall;

my $DEBUG = 1;

# Configuration variables.
my $dataDir = $CONFIG{data_dir};    # The path containing the source data.
my $insertTable
    = $CONFIG{insert_table};    # The table into which data should be inserted.

# Process each data file in a directory.
# Insert data to a PostgreSQL DB.

my %colAssoc = (); # Hash for mapping between DB columns and CSV columns.
my %egMap;         # Hash for mapping between egauge numbers and house numbers.

my @files;         # Array to hold the data files that are going to be read.
my $dbname;        # Name of the database.
my $DBH;           # Global database handle used by DBI.
my @headerItems     = ();    # An array of the columns in the header.
my @columnsToInsert = ();    # SQL columns to be inserted
my $sql             = "";    # Holds the SQL statement.
my $validHeader; # Flag for indicating that the source data has a valid header.
my $sth;         # DBI statement handle.
my $dateDataColumn
    = -1;        # Index for data column containing the date of the record.
my $houseIDColumn = -1;
my $idCol = "egauge_id";

######################################################################
# END VARIABLES                                                      #
######################################################################

###
# Given a filename, return the egauge number.
#
# @param filename
# @return egauge number based on house number
##
sub getEgaugeNumber {
    my ($filename) = @_;
	#print "filename = $filename\n" if $DEBUG;
    #if ( $filename =~ m/(.*)\/egauge(.*)\.csv/i ) {
	if ( $filename =~ m/^(.*)\/(\d+)\.csv/i) {
        return $2;
    }
}

###
# For all the cols located in a CSV, match them to the mapped columns.
#
# @param header: text of the header
# @return 1|0 indicating a valid header
##
sub readHeader {
    my ($header) = @_;

    if ($header) {
        @headerItems = split( ',', $header );    # split on commas

        print STDERR "header = $header\n" if $DEBUG;

    }
    else {
        print "ERROR: no header\n";
        return 0;
    }

    # Translate data header items to SQL columns.
    foreach my $item (@headerItems) {

        if ( $item =~ s/\R//g ) { }  # critical: remove linefeeds of all types
        if ( $item =~ s/\"//g ) {
        } # critical: need to remove quote symbols in order to match hash items

        if ($DEBUG) {
            #print "colAssoc = ";
            #print %colAssoc;
            #print "\n";
        }

        print "item = $item\n" if $DEBUG;
        if ( defined( $colAssoc{$item} ) ) {
            push( @columnsToInsert, $colAssoc{$item} );
        }    # If it doesn't match, then don't do anything.
        else {
            print "ERROR: nonmatching column: ";
            print $colAssoc{$item};
            print " does not match\n";
            exit;
        }
    }
    return 1;
}

###
# Check if a database record exists using the primary keys
# @param house id
# @param datetime
##
sub checkRecordExists {
    my ( $house_id, $datetime ) = @_;
    my $sql
        = "select $idCol, datetime from $insertTable where $idCol = ? AND datetime = ?";
    my $sth    = $DBH->prepare($sql);
    my $result = $sth->execute();
    print "result = $result\n" if $DEBUG;
}

sub filteredEgaugeNumber {
	my ($filename) = @_;
	if ($filename =~ /^(\d+)$/) {
		return $1;
	}
	else {
		return "MISSING";
	}
}


######################################################################
# END SUBROUTINES                                                    #
######################################################################

# ************************************************************************************
# ***   START OF DATA PROCESSING                                                   ***
# ************************************************************************************

$DBH      = DZSEPLib::connectDatabase( $CONFIG{fc_dbname}, $CONFIG{db_host},
                                      $CONFIG{db_port}, $CONFIG{db_user}, $CONFIG{db_pass} );
#%egMap    = %{ DZSEPLib::mapEgaugeNumbersToHouseID() };
%colAssoc = %{ DZSEPLib::mapCSVColumnsToDatabaseColumns() };

my @data = ();
my $result;
my $currentDataColumn;
my $dataLine;
my $lineCanBeInserted;

my $checkHouseId;     # Used for checking the existence of a record.
my $checkDatetime;    # Used for checking the existence of a record.

my $currentDatetime;
my $currentHouseID;
my $currentEgaugeID;

my $FATAL_ERROR = 0;

my $egaugeNumber;

###
# Iterate through each file containing data and insert the data into the database.
#
# @param array reference of files to process
##
sub insertDataInDataDirectory {
    my ($filesRef) = @_;
    foreach my $f ( sort @{$filesRef} ) {    # For each data file...
        my $cmd = "";

		$egaugeNumber = getEgaugeNumber($f);
        print "\negauge number = $egaugeNumber\n";

        #print ", house id = ";
        #print $egMap{ getEgaugeNumber($f) };

        # Read the data in the file.

        print STDERR "Reading file $f...\n";
        open( FILE, "<$f" );
        @data = <FILE>;
        close(FILE);

        $validHeader = 0;
        my $headerColumnCount = 0;
        @columnsToInsert = ();
        my $sql = "INSERT INTO $insertTable (";

        $sql .= "$idCol, ";

        # Process the header in the data file.
        @columnsToInsert = ();
        $validHeader
            = readHeader( $data[0] );    # Check the header of the data file.
        $dateDataColumn = -1;            # Initalize the date column.

        # Load each column into the SQL statement.
        for my $col ( 0 .. $#columnsToInsert ) {
            if ( $columnsToInsert[$col] eq "datetime" ) {
                $dateDataColumn = $col;    # Found a datetime column.
            }

            $sql .= "$columnsToInsert[$col]";
            $headerColumnCount++;
            $sql .= ", ";
        }

        if ( $dateDataColumn < 0 && $validHeader ) {
            die "ERROR: found no datetime column";
        }

        $sql .= "upload_date";
        $sql .= ") VALUES (";

        my $sqlFront = $sql;
        my $sqlBack  = ""; # Declaraction and assignment to empty string.
        #my $houseId  = $egMap{ getEgaugeNumber($f) };

        # Data is processed by file by file.
        #
        # If there's a valid header then the data can be inserted into the database.
        if ($validHeader) {

            my $cnt = 0;
            $lineCanBeInserted = 0;

            # Use the SQL statements to insert the data.
            $dataLine = 0;

            # Now, the individual lines of a data file are being processed.
            foreach my $line (@data) {

				# Start building the end of the SQL statement where the data values are located, the SQL Back.
                $sqlBack           = "$egaugeNumber,";
                $currentDataColumn = 0;

                if ( $cnt > 0 ) {    # skip header
                    $lineCanBeInserted = 1;

                    # Do something with the line of data.
                    my @dataColumns = split( /,/, $line );
                    foreach my $value (@dataColumns) {
                        if ( $value =~ s/\R//g ) { }    # remove linefeed

                        # The datetime column is handled differently.
                        # It contains the timestamp for the data record.
                        if ( $currentDataColumn == $dateDataColumn ) {
                            $sqlBack .= "to_timestamp($value),"
                                ;    # Change to PostgreSQL timestamp.
                            $currentDatetime = $value;
                        }
                        else {
                            $sqlBack .= "abs($value),";
                        }

                        $currentDataColumn++;
                    }
                }    # End if.

                $cnt++;

        		# This is a timestamp for when a record is inserted into the database.
                $sqlBack .= "to_timestamp("
                    . time() . ") ";

                $sqlBack .= ");";    # End of the SQL statement.

                $sql = "$sqlFront$sqlBack";

                # Check if the record exists.
                if (DZSEPLib::msgEnergyRecordExists(
                        $insertTable, $egaugeNumber, $currentDatetime
                    ))
                {
                    $lineCanBeInserted = 0;
                }

                if ($lineCanBeInserted) {
                    print "sql = $sql\n" if $DEBUG;

                    $sth = $DBH->prepare($sql);

                    $result = $sth->execute();

                    # Check for error conditions.
                    if ( !$result ) {
                        $FATAL_ERROR = 1;
                    }
                    else {
                        if ( $result eq "0E0" ) {
                            $FATAL_ERROR = 1;
                        }
                    }
                    if ($FATAL_ERROR) {
                        die
                            "FATAL ERROR (insert aborted): line = $dataLine, sql=$sql\n";
                    }
                }
                $dataLine++;
            }    # End foreach.
        }
        $DBH->commit();
        print "finished processing file.\n";
    }    # End foreach.
}

# Get all directories having data that needs to be loaded.
my @dirs = ();
if ( -d $dataDir ) {
    print "valid directory\n";
    @dirs = grep {-d} glob "$dataDir/*";
}

if ($DEBUG) {
    print "dirs = ";
    print @dirs;
    print "\n";
}

# Go through each dir and push the files to be processed into an array.
foreach my $d (@dirs) {
    print $d;
    print "\n";

    # Change the directory to the data directory.
    print "Loading data in \"$d\"...\n";

    opendir( DIR, "$d" ) or die $!;

    while ( my $file = readdir(DIR) ) {
        if ( $file =~ /^.*\.csv$/ ) {
            push( @files, "$d/$file" );
        }
    }
}

# Iterate through each directory and file containing data in the data directory.
insertDataInDataDirectory( \@files );

# Data has now been successfully inserted because the insertion routine fails on all errors.
# Therefore, move the data files to the loaded data directory.
if ( ! chdir( $CONFIG{data_dir} ) ) {
    die "Couldnt change to data dir " . $CONFIG{data_dir} . "\n";
}

foreach my $d (@dirs) {
    print "directory = $d\n";
    my $baseName = basename($d);
    print "basename = $baseName\n";
    DZSEPLib::moveReliable( $baseName, $CONFIG{loaded_data_dir} );
}

exit;
