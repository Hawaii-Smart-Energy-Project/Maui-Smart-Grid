#!/usr/bin/env python -u
# -*- coding: utf-8 -*-

"""
Usage:

time python -u ${PATH}/insertData.py ${FILENAME} > ${LOG_FILE}

"""

__author__ = 'Daniel Zhang (張道博)'

from mecoxmlparser import MECOXMLParser
import glob
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

    def __init__(self):
        """
        Constructor.
        """

        self.parser = MECOXMLParser()
        self.configer = MECOConfiger()


parser = argparse.ArgumentParser(
    description = 'Perform insertion of data contained in a single file to '
                  'the MECO database specified in the configuration file.')

parser.add_argument('--filepath',
                    help = 'A filepath, including the filename, '
                           'for a file containing data to be inserted.')

args = parser.parse_args()

if (args.filepath):
    print "Processing %s." % args.filepath
else:
    print "Usage: insertData ${FILEPATH}"
    sys.exit(-1)

filepath = args.filepath

i = Inserter()

if i.configer.configOptionValue("Debugging", "debug"):
    print "Debugging is on"

sys.stderr.write("Inserting data to database %s." % \
                 i.configer.configOptionValue("Database", "db_name"))

# path = '.'

# Process all of the XML files in the current directory.
# data = glob.glob("%s/*.xml*" % path)

# data.sort()
# for f in data:
#     print f
#     if re.search('.*log\.xml', f) is None: # skip *log.xml files

filename = os.path.basename(filepath)
fileObject = None
# Open the file and read it.
if re.search('.*\.xml$', filepath):
    fileObject = open(filepath, "rb")
elif re.search('.*\.xml\.gz$', filepath):
    fileObject = gzip.open(filepath, "rb")
else:
    print "Error: %s is not an XML file." % filepath
i.parser.filename = args.filepath
i.parser.parseXML(fileObject, True)
fileObject.close()
