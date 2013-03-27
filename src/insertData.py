#!/usr/bin/env python -u
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'

from mecoxmlparser import MECOXMLParser
import glob
import re
from mecoconfig import MECOConfiger

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

# process all XML files
data = glob.glob("./*.xml")

data.sort()
for f in data :
    if re.search('.*log\.xml', f) is None :
        i.parser.filename = f
        i.parser.parseXML(True)


