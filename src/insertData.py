#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Usage:

time python -u ${PATH}/insertData.py --filepath ${FILEPATH} [--testing] > ${LOG_FILE}

This script is used by recursivelyInsertData.py.
"""

__author__ = 'Daniel Zhang (張道博)'

from mecoxmlparser import MECOXMLParser
import re
from mecoconfig import MECOConfiger
import gzip
import sys
import argparse
import os


class Inserter(object):
    """
    Perform insertion of data contained in a single file to the MECO database
    specified in the configuration file.
    """

    def __init__(self, testing=False):
        """
        Constructor.

        :param testing: Flag indicating if testing mode is on.
        """

        self.parser = MECOXMLParser(testing)
        self.configer = MECOConfiger()


parser = argparse.ArgumentParser(
    description = 'Perform insertion of data contained in a single file to '
                  'the MECO database specified in the configuration file.')

parser.add_argument('--filepath',
                    help = 'A filepath, including the filename, '
                           'for a file containing data to be inserted.')
parser.add_argument('--testing', action = 'store_true',
                    help = 'Insert data to the testing database as specified '
                           'in the local configuration file.')

args = parser.parse_args()

if (args.filepath):
    print "Processing %s." % args.filepath
else:
    print "Usage: insertData --filepath ${FILEPATH} [--testing]"
    sys.exit(-1)

filepath = args.filepath

i = Inserter(args.testing)

if i.configer.configOptionValue("Debugging", "debug"):
    print "Debugging is on"

sys.stderr.write("\nInserting data to database %s.\n" % \
                 i.configer.configOptionValue("Database", "db_name"))

filename = os.path.basename(filepath)
fileObject = None

# Open the file and process it.
if re.search('.*\.xml$', filepath):
    fileObject = open(filepath, "rb")
elif re.search('.*\.xml\.gz$', filepath):
    fileObject = gzip.open(filepath, "rb")
else:
    print "Error: %s is not an XML file." % filepath
i.parser.filename = args.filepath
i.parser.parseXML(fileObject, True)
fileObject.close()
