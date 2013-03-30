#!/usr/bin/env python -u
# -*- coding: utf-8 -*-

"""
Usage:

time python -u ${PATH}/insertData.py > ${LOG_FILE}

"""

__author__ = 'Daniel Zhang (張道博)'

from mecoxmlparser import MECOXMLParser
import glob
import re
from mecoconfig import MECOConfiger
import gzip
import sys

class Inserter(object) :
    """Perform insertion of data to the MECO DB.
    """

    def __init__(self) :
        """Constructor"""
        self.parser = MECOXMLParser()
        self.configer = MECOConfiger()

i = Inserter()

if i.configer.configOptionValue("Debugging","debug"):
    print "Debugging is on"

sys.stderr.write("Inserting data to database %s." % \
      i.configer.configOptionValue("Database","db_name"))

path = '.'

# process all XML files
data = glob.glob("%s/*.xml*" % path)

data.sort()
for f in data :
    print f
    if re.search('.*log\.xml', f) is None: # skip *log.xml files

        # open the file and read it
        if re.search('.*\.xml$', f):
            fileObject = open(f, "rb")
        elif re.search('.*\.xml\.gz$', f):
            fileObject = gzip.open(f, "rb")
        else:
            print "Error: No XML files were matched in %s." % path
        i.parser.filename = f
        i.parser.parseXML(fileObject, True)
        fileObject.close()
