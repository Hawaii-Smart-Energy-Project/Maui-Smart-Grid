#!/usr/bin/env python -u
# -*- coding: utf-8 -*-

"""
Usage:

time python -u ${PATH}/recursivelyInsertData.py > ${LOG_FILE}

From the current directory, recursively descend into every existing folder and
insert all data that is found.

This script makes use of insertData.py.

This script only supports processing of *.xml.gz files.
"""

__author__ = 'Daniel Zhang (張道博)'

import os
import fnmatch
import sys
from subprocess import call
from mecoconfig import MECOConfiger
import re

xmlGzCount = 0
xmlCount = 0
configer = MECOConfiger()
binPath = MECOConfiger.configOptionValue(configer, "Executable Paths",
                                         "bin_path")

print "Recursively inserting data."

startingDirectory = os.getcwd()
print "Starting in %s." % startingDirectory

for root, dirnames, filenames in os.walk('.'):

    for filename in fnmatch.filter(filenames, '*.xml'):
        fullPath = os.path.join(root, filename)
        print fullPath
        xmlCount += 1

if xmlCount != 0:
    print "Found XML files that are not gzip compressed.\nUnable to proceed."
    sys.exit(-1)

insertScript = "%s/insertData.py" % binPath
print "insertScript = %s" % insertScript

try:
    with open(insertScript):
        pass
except IOError:
    print "Insert script %s not found." % insertScript

for root, dirnames, filenames in os.walk('.'):
    for filename in fnmatch.filter(filenames, '*.xml.gz'):
        if re.search('.*log\.xml', filename) is None: # skip *log.xml files

            fullPath = os.path.join(root, filename)
            print fullPath
            xmlGzCount += 1

            # Execute the insert data script for the file.
            call([insertScript, "--filepath", fullPath])

print "%s files were processed." % xmlGzCount
