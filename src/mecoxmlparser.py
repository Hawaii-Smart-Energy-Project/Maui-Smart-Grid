#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'

import xml.etree.ElementTree as ET
import re
from mecodbinsert import MECODBInserter
from mecoconfig import MECOConfiger
from mecodbutils import MECODBUtil
from mecomapper import MECOMapper
from mecodbconnect import MECODBConnector
from meco_fk import MECOFKDeterminer
import sys
from itertools import tee, islice, izip_longest
from mecodupecheck import MECODupeChecker

DEBUG = 1 # print debugging info if 1

class MECOXMLParser(object) :
    """Parses XML for MECO data.
    """

    tableName = ''

    def __init__(self) :
        """Constructor
        """

        self.mecoConfig = MECOConfiger()
        self.util = MECODBUtil()
        self.mapper = MECOMapper()
        self.connector = MECODBConnector()
        self.conn = self.connector.connectDB()

        self.filename = None
        self.elementCount = 0
        self.inserter = MECODBInserter()
        self.insertDataIntoDatabase = False

        # count how many times sections in source data are encountered
        self.tableNameCount = {'SSNExportDocument' : 0, 'MeterData' : 0, 'RegisterData' : 0,
                               'RegisterRead' : 0, 'Tier' : 0, 'Register' : 0,
                               'IntervalReadData' : 0, 'Interval' : 0, 'Reading' : 0,
                               'IntervalStatus' : 0, 'ChannelStatus' : 0}

        # @todo adjust test to handle interval status and channel status

        self.insertTables = self.mecoConfig.insertTables

        self.lastSeqVal = None
        self.fKeyVal = None
        self.lastTable = None
        self.fkDeterminer = MECOFKDeterminer()
        self.dupeChecker = MECODupeChecker()
        self.currentMeterName = None
        self.dupesExist = False

    def parseXML(self, insert = False) :
        """Parse an XML file.
        :param insert - True to insert to the database | False to perform no inserts
        """

        print "parseXML:"

        self.insertDataIntoDatabase = insert
        print "parsing xml in", self.filename
        tree = ET.parse(self.filename)
        root = tree.getroot()
        self.walkTheTreeFromRoot(root)

    def walkTheTreeFromRoot(self, root) :
        """Walk an XML tree from its root node.
        :param root Root node of an XML tree.
        """

        walker = root.iter()

        for element, nextElement in self.getNext(walker):
            self.elementCount += 1

            currentTableName = re.search('\{.*\}(.*)', element.tag).group(1) # current table name
            try:
                nextTableName = re.search('\{.*\}(.*)', nextElement.tag).group(1) # next table name
            except:
                if DEBUG:
                    print "EXCEPTION: nextElement = %s" % nextElement
                nextTableName = None

            self.tableNameCount[currentTableName] += 1

            columnsAndValues = {}
            it = iter(sorted(element.attrib.iteritems()))

            for item in list(it) :
                # Create a dictionary of column names and values.
                columnsAndValues[item[0]] = item[1]

            if currentTableName in self.insertTables :
                if DEBUG:
                    print
                    print "processing table %s, next is %s" % (currentTableName, nextTableName)
                    print "--------------------------------"

                pkeyCol = self.mapper.dbColumnsForTable(currentTableName)[
                          '_pkey'] # get the col name for the pkey
                fkeyCol = None
                fKeyValue = None

                try :
                    fkeyCol = self.mapper.dbColumnsForTable(currentTableName)[
                              '_fkey'] # get the col name for the fkey
                except :
                    pass

                if DEBUG:
                    print "foreign key col (fkey) = %s" % fkeyCol
                    print "primary key col (pkey) = %s" % pkeyCol
                    print columnsAndValues

                # get fk value
                if fkeyCol is not None :
                    fKeyValue = self.fkDeterminer.pkValforCol[fkeyCol]

                if DEBUG:
                    print "fKeyValue = %s" % fKeyValue

                if currentTableName == "MeterData":
                    self.currentMeterName = columnsAndValues['MeterName']

                # perform a dupe check for the reading branch
                if currentTableName == "Interval" :
                    print "end time value = %s" % columnsAndValues['EndTime']
                    if (self.dupeChecker.meterNameAndEndTimeExists(
                            self.currentMeterName,
                            columnsAndValues['EndTime']) == True
                    ) :
                        self.dupesExist = True
                        if DEBUG:
                            print "dupe check = True"
                    else :
                        if DEBUG:
                            print "dupe check = False"

                if self.insertDataIntoDatabase == True :
                    cur = self.inserter.insertData(self.conn, currentTableName,
                                                   columnsAndValues, fKeyValue,
                                                   1) # last 1 indicates don't commit

                self.lastSeqVal = self.util.getLastSequenceID(self.conn, currentTableName,
                                                              pkeyCol)
                # store pk
                self.fkDeterminer.pkValforCol[pkeyCol] = self.lastSeqVal

                if DEBUG:
                    print "lastSeqVal = ", self.lastSeqVal


                if self.lastReading(currentTableName, nextTableName):
                    if DEBUG:
                        print "----- last reading found -----"

                    sys.stdout.write('.')
                    sys.stdout.write("(%s)" % self.elementCount)

                    # before committing, are there any duplicates?
                    if self.dupesExist :
                        self.conn.rollback()
                        if DEBUG:
                            print "(dupe(s) found... performing rollback...)"
                        self.dupesExist = False
                    else :
                        self.conn.commit()

                if self.lastRegister(currentTableName, nextTableName):
                    if DEBUG:
                        print "----- last register found -----"

        self.conn.commit()
        print

    def lastReading(self, currentTable, nextTable):
        """Determine if the last reading is being visited.
        :return True if last object in Reading table was read, otherwise return False.
        """
        if currentTable == "Reading" and (
                nextTable == "MeterData" or nextTable == None) :
            return True
        return False

    def lastRegister(self, currentTable, nextTable):
        """Determine if the last register is being visited.
        :return True if last object in Register table was read, otherwise return False.
        """
        if currentTable == "Register" and (
                nextTable == "MeterData" or nextTable == None) :
            return True
        return False

    def getNext(self, somethingIterable, window=1):
        """Return the current item and next item in an iterable data structure.
        :param somethingIterable something that has an iterator
        :param window
        :return value and next value
        """
        items, nexts = tee(somethingIterable, 2)
        nexts = islice(nexts, window, None)
        return izip_longest(items, nexts)
