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
from meconotifier import MECONotifier

xmlGzCount = 0
xmlCount = 0
configer = MECOConfiger()
binPath = MECOConfiger.configOptionValue(configer, "Executable Paths",
                                         "bin_path")
msgBody = ''
notifier = MECONotifier()

msg = "Recursively inserting data."
print msg
msgBody += msg + "\n"

startingDirectory = os.getcwd()
msg = "Starting in %s." % startingDirectory
print msg
msgBody += msg + "\n"

for root, dirnames, filenames in os.walk('.'):

    for filename in fnmatch.filter(filenames, '*.xml'):
        fullPath = os.path.join(root, filename)
        msg = fullPath
        print msg
        msgBody += msg + "\n"
        xmlCount += 1

if xmlCount != 0:
    msg = "Found XML files that are not gzip compressed.\nUnable to proceed."
    print msg
    msgBody += msg + "\n"
    notifier.sendNotificationEmail(msgBody)
    sys.exit(-1)

insertScript = "%s/insertData.py" % binPath
msg = "insertScript = %s" % insertScript
print msg
msgBody += msg + "\n"

try:
    with open(insertScript):
        pass
except IOError:
    msg = "Insert script %s not found." % insertScript
    print msg
    msgBody += msg + "\n"

for root, dirnames, filenames in os.walk('.'):
    for filename in fnmatch.filter(filenames, '*.xml.gz'):
        if re.search('.*log\.xml', filename) is None: # skip *log.xml files

            fullPath = os.path.join(root, filename)
            msg = fullPath
            print msg
            msgBody += msg + "\n"
            xmlGzCount += 1

            # Execute the insert data script for the file.
            call([insertScript, "--filepath", fullPath])

msg = "%s files were processed." % xmlGzCount
print msg
msgBody += msg + "\n"
notifier.sendNotificationEmail(msgBody)
