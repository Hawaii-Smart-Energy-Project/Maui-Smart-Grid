#!/usr/bin/env perl

# With MECO export data, substitute values so they are meaningless.
# This test data is used during unit testing.
#
# @author Daniel Zhang (張道博)

use strict;
use English qw(-no_match_vars);

my $filename = $ARGV[$0];
if ( !$filename ) {
    print "Usage: createTestMECOData.pl \$FILENAME\n";
    exit;
}
print STDERR "Processing $filename\n";
open( FILE, "<$filename" );
my @data = <FILE>;

foreach my $line (@data) {
    my $rand     = rand(5000);

    if ( $line =~ /Summation=\"(.*)\"\s+/i ) {
        $line = replaceCaptureGroup( $line, $rand );
    }
    if ( $line =~ /BlockEndValue=\"(.*)\"\//i ) {
        $line = replaceCaptureGroup( $line, $rand );
    }
    if ( $line =~ /RawValue=\"(.*)\"\s+/i ) {
        $line = replaceCaptureGroup( $line, int($rand) );
    }
    if ( $line =~ /CumulativeDemand=\"(.*)\"\s+/i ) {
        $line = replaceCaptureGroup( $line, $rand );
    }

    print $line;
}
close(FILE);

###
# @param string containing capture group
# @param replacement string
# @return new string
##
sub replaceCaptureGroup {
    my ( $string, $replacement ) = @_;
    substr $string, $LAST_MATCH_START[1],
        $LAST_MATCH_END[1] - $LAST_MATCH_START[1], $replacement;
    return $string;
}
