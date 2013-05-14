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

DEBUG = 0 # print debugging info if 1


class MECOXMLParser(object):
    """Parses XML for MECO data.
    """

    tableName = ''

    def __init__(self, testing = False):
        """
        Constructor.

        :param testing: (optional) Boolean indicating if Testing Mode is on.
        """

        if (testing):
            print "Testing Mode is ON."

        self.configer = MECOConfiger()
        self.util = MECODBUtil()
        self.mapper = MECOMapper()
        self.connector = MECODBConnector(testing)
        self.conn = self.connector.connectDB()
        self.filename = None
        self.fileObject = None
        self.elementCount = 0
        self.inserter = MECODBInserter()
        self.insertDataIntoDatabase = False

        # Count number of times sections in source data are encountered.
        self.tableNameCount = {'SSNExportDocument': 0, 'MeterData': 0,
                               'RegisterData': 0, 'RegisterRead': 0,
                               'Tier': 0, 'Register': 0,
                               'IntervalReadData': 0, 'Interval': 0,
                               'Reading': 0, 'IntervalStatus': 0,
                               'ChannelStatus': 0, 'EventData': 0,
                               'Event': 0}

        # @todo adjust unit test to handle interval status and channel status

        # Use this dictionary to track which channels were processed when
        # readings are being processed. this is to prevent duplicate channel
        # data from being inserted.
        self.channelProcessed = {}

        self.initChannelProcessed()
        self.processingReadingsNow = False

        # Tables to be inserted to.
        self.insertTables = self.configer.insertTables

        self.lastSeqVal = None
        self.fKeyVal = None
        self.lastTable = None
        self.fkDeterminer = MECOFKDeterminer()
        self.dupeChecker = MECODupeChecker()
        self.currentMeterName = None
        self.currentIntervalEndTime = None
        self.dupesExist = False
        self.channelDupeExists = False
        self.commitCount = 0
        self.dupeOnInsertCount = 0

    def parseXML(self, fileObject, insert = False):
        """
        Parse an XML file.

        :param fileObject: a file object referencing an XML file.
        :param insert: (optional) True to insert to the database | False to
        perform no
        inserts.
        """

        print "parseXML:"

        self.commitCount = 0
        self.insertDataIntoDatabase = insert
        sys.stderr.write("\nparsing xml in %s\n" % self.filename)
        tree = ET.parse(fileObject)
        root = tree.getroot()
        self.walkTheTreeFromRoot(root)


    def walkTheTreeFromRoot(self, root):
        """
        Walk an XML tree from its root node.

        :param root: The root node of an XML tree.
        """

        walker = root.iter()

        for element, nextElement in self.getNext(walker):
            self.elementCount += 1

            currentTableName = re.search('\{.*\}(.*)', element.tag).group(
                1)
            try:
                nextTableName = re.search('\{.*\}(.*)', nextElement.tag).group(
                    1)
            except:
                if self.configer.configOptionValue("Debugging",
                                                   'debug') == True:
                    print "EXCEPTION: nextElement = %s" % nextElement
                nextTableName = None

            self.tableNameCount[currentTableName] += 1

            columnsAndValues = {}
            it = iter(sorted(element.attrib.iteritems()))

            for item in list(it):
                # Create a dictionary of column names and values.
                columnsAndValues[item[0]] = item[1]

            if currentTableName in self.insertTables:
                # Check if the current table is one of the tables to be
                # inserted to.

                if self.configer.configOptionValue("Debugging",
                                                   'debug') == True:
                    print
                    print "Processing table %s, next is %s." % (
                        currentTableName, nextTableName)
                    print "--------------------------------"

                # Get the column name for the primary key.
                pkeyCol = self.mapper.dbColumnsForTable(currentTableName)[
                    '_pkey']

                fkeyCol = None
                fKeyValue = None

                try:
                    # Get the column name for the foreign key.
                    fkeyCol = self.mapper.dbColumnsForTable(currentTableName)[
                        '_fkey']
                except:
                    pass

                if self.configer.configOptionValue("Debugging",
                                                   'debug') == True:
                    print "foreign key col (fkey) = %s" % fkeyCol
                    print "primary key col (pkey) = %s" % pkeyCol
                    print columnsAndValues

                if fkeyCol is not None:
                    # Get the foreign key value.
                    fKeyValue = self.fkDeterminer.pkValforCol[fkeyCol]

                if self.configer.configOptionValue("Debugging",
                                                   'debug') == True:
                    print "fKeyValue = %s" % fKeyValue

                if currentTableName == "MeterData":
                    self.currentMeterName = columnsAndValues['MeterName']

                # Perform a dupe check for the Reading branch.
                if currentTableName == "Interval":
                    self.currentIntervalEndTime = columnsAndValues['EndTime']

                if currentTableName == "Event":
                    columnsAndValues['Event_Content'] = element.text;

                if self.insertDataIntoDatabase:

                    # Handle a special case for duplicate reading data.
                    # Intercept the duplicate reading data before insert.
                    if currentTableName == "Reading":
                        # does a meter-endtime-channel dupe exist?
                        self.channelDupeExists \
                            = self.dupeChecker.readingBranchDupeExists(
                            self.conn,
                            self.currentMeterName,
                            self.currentIntervalEndTime,
                            columnsAndValues['Channel']
                        )

                    # Only perform an insert if there are no duplicate values
                    # for the channel.
                    if not self.channelDupeExists:
                        cur = self.inserter.insertData(self.conn,
                                                       currentTableName,
                                                       columnsAndValues,
                                                       fKeyValue,
                                                       1)
                    # The last 1 indicates don't commit.

                    else: # Don't insert into Reading table if a dupe exists.
                        print "Duplicate meter-endtime-channel exists."
                        self.dupeOnInsertCount += 1
                        if self.dupeOnInsertCount > 0 and self \
                            .dupeOnInsertCount < 2:
                            sys.stderr.write("{dupe on insert==>}")

                        # Also, verify the data is equivalent to the existing
                        # record.
                        if self.dupeChecker.readingValuesAreInTheDatabase(
                                self.conn,
                                columnsAndValues):
                            print "Verified reading values are in the database"

                        self.channelDupeExists = False

                self.lastSeqVal = self.util.getLastSequenceID(self.conn,
                                                              currentTableName,
                                                              pkeyCol)
                # Store the primary key.
                self.fkDeterminer.pkValforCol[pkeyCol] = self.lastSeqVal

                if self.configer.configOptionValue("Debugging",
                                                   'debug') == True:
                    print "lastSeqVal = ", self.lastSeqVal

                if self.lastReading(currentTableName, nextTableName):
                    if self.configer.configOptionValue("Debugging",
                                                       'debug') == True:
                        print "----- last reading found -----"

                    self.conn.commit()

                    sys.stderr.write("{%s}" % self.dupeOnInsertCount)
                    sys.stderr.write("[%s]" % self.commitCount)
                    sys.stderr.write("(%s)" % self.elementCount)

                    self.commitCount += 1
                    self.dupeOnInsertCount = 0

                    if self.configer.configOptionValue("Debugging",
                                                       "limit_commits") and \
                                    self.commitCount > 8:
                        self.commitCount = 0
                        return

                if self.lastRegister(currentTableName, nextTableName):
                    if self.configer.configOptionValue("Debugging",
                                                       'debug') == True:
                        print "----- last register found -----"

        self.conn.commit()
        print


    def lastReading(self, currentTable, nextTable):
        """
        Determine if the last reading is being visited.

        :param currentTable: current table being processsed.
        :param nextTable: next table to be processed.
        :returns: True if last object in Reading table was read,
        otherwise return False.
        """

        if currentTable == "Reading" and (
                    nextTable == "MeterData" or nextTable == None):
            return True
        return False


    def lastRegister(self, currentTable, nextTable):
        """Determine if the last register is being visited.

        :param currentTable: current table being processsed.
        :param nextTable: next table to be processed.
        :returns: True if last object in Register table was read,
        otherwise return False.
        """

        if currentTable == "Register" and (
                    nextTable == "MeterData" or nextTable == None):
            return True
        return False


    def getNext(self, somethingIterable, window = 1):
        """
        Return the current item and next item in an iterable data structure.

        :param somethingIterable: Something that has an iterator.
        :param window: How far to look ahead in the collection.
        :returns: The current iterable value and the next iterable value.
        """

        items, nexts = tee(somethingIterable, 2)
        nexts = islice(nexts, window, None)
        return izip_longest(items, nexts)


    def initChannelProcessed(self):
        """
        Initialize the dictionary for channel processing.
        """

        self.channelProcessed = {'1': False, '2': False, '3': False,
                                 '4': False}


    def getLastElement(self, rows):
        """
        Get the last element in a collection.

        Example:
            rows = (element1, element2, element3)
            getLastElement(rows) # return element3

        :param rows: Result rows from a query.
        :returns: The last element in the collection.
        """

        for i, var in enumerate(rows):
            if i == len(rows) - 1:
                return var


    def performRollback(self):
        self.conn.rollback()
