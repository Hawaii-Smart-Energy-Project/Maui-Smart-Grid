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
from mecologger import MECOLogger

DEBUG = 0 # print debugging info if 1


class MECOXMLParser(object):
    """
    Parses XML for MECO data.
    """

    tableName = ''

    def __init__(self, testing = False):
        """
        Constructor.

        :param testing: (optional) Boolean indicating if Testing Mode is on.
        """

        self.logger = MECOLogger(__name__, 'silent')

        if (testing):
            self.logger.log("Testing Mode is ON.", 'info')

        self.debug = False
        self.configer = MECOConfiger()
        if self.configer.configOptionValue("Debugging",
                                           'debug') == True:
            self.debug = True

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
        self.dataProcessCount = 0

    def parseXML(self, fileObject, insert = False):
        """
        Parse an XML file.

        :param fileObject: a file object referencing an XML file.
        :param insert: (optional) True to insert to the database | False to
        perform no
        inserts.
        :returns: String containing a concise log of parsing.
        """

        print "parseXML:"

        self.commitCount = 0
        self.insertDataIntoDatabase = insert

        parseMsg = "\nParsing XML in %s.\n" % self.filename
        sys.stderr.write(parseMsg)
        parseLog = parseMsg

        tree = ET.parse(fileObject)
        root = tree.getroot()

        parseLog += self.walkTheTreeFromRoot(root)

        return parseLog


    def tableNameForAnElement(self, element):
        """
        Get the tablename for an element.

        :param element: Element tree element.
        :returns: table name
        """

        name = ''
        try:
            name = re.search('\{.*\}(.*)', element.tag).group(1)
        except:
            name = None
        return name


    def processDataToBeInserted(self, columnsAndValues, currentTableName,
                                fKeyValue, parseLog, pkeyCol):
        """
        This is the method that performs insertion of parsed data to the
        database.

        :param columnsAndValues: A dictionary containing columns and their
        values.
        :param currentTableName: The name of the current table.
        :param fKeyValue: The value of the foreign key.
        :param parseLog: String containing a concise log of operations.
        :param pkeyCol: Column name for the primary key.
        :returns: A string containing the parse log.
        """

        self.dataProcessCount += 1

        # Handle a special case for duplicate reading data.
        # Intercept the duplicate reading data before insert.
        if currentTableName == "Reading":
            # Does a meter-endtime-channel tuple duplicate exist?
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
            # ***********************
            # ***** INSERT DATA *****
            # ***********************
            cur = self.inserter.insertData(self.conn,
                                           currentTableName,
                                           columnsAndValues,
                                           fKeyValue,
                                           1)
            # The last 1 indicates don't commit. Commits are handled externally.

            # If no insertion took place,
            # don't attempt to get the last sequence value.
            self.lastSeqVal \
                = self.util.getLastSequenceID(self.conn,
                                              currentTableName,
                                              pkeyCol)
            # Store the primary key.
            self.fkDeterminer.pkValforCol[pkeyCol] = self.lastSeqVal


        else: # Don't insert into Reading table if a dupe exists.
            print "Duplicate meter-endtime-channel exists."
            self.dupeOnInsertCount += 1
            if self.dupeOnInsertCount > 0 and self \
                .dupeOnInsertCount < 2:
                parseLog += self.logger.logAndWrite("{dupe on insert==>}")

            # Also, verify the data is equivalent to the existing
            # record.
            matchingValues = self.dupeChecker.readingValuesAreInTheDatabase(
                self.conn, columnsAndValues)
            if matchingValues:
                print "Verified reading values are in the database."
            assert (matchingValues == True, "Duplicate check found non-matching values.")

            self.channelDupeExists = False
        return parseLog

    def walkTheTreeFromRoot(self, root):
        """
        Walk an XML tree from its root node.

        :param root: The root node of an XML tree.
        :returns: String containing a concise log of parsing activity.
        """

        parseLog = ''
        parseMsg = ''
        walker = root.iter()

        for element, nextElement in self.getNext(walker):
            # Process every element in the tree while reading ahead to get
            # the next element.

            self.elementCount += 1

            currentTableName = self.tableNameForAnElement(element)
            nextTableName = self.tableNameForAnElement(nextElement)
            assert (currentTableName is not None)

            # Maintain a count of tables encountered.
            self.tableNameCount[currentTableName] += 1

            columnsAndValues = {}
            it = iter(sorted(element.attrib.iteritems()))

            for item in list(it):
                # Create a dictionary of column names and values.
                columnsAndValues[item[0]] = item[1]

            if currentTableName in self.insertTables:
                # Check if the current table is one of the tables to have data
                # inserted.

                if self.debug:
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

                if self.debug:
                    print "foreign key col (fkey) = %s" % fkeyCol
                    print "primary key col (pkey) = %s" % pkeyCol
                    print columnsAndValues

                if fkeyCol is not None:
                    # Get the foreign key value.
                    fKeyValue = self.fkDeterminer.pkValforCol[fkeyCol]

                if self.debug:
                    print "fKeyValue = %s" % fKeyValue

                # Perform table based operations.
                if currentTableName == "MeterData":
                    self.currentMeterName = columnsAndValues['MeterName']

                if currentTableName == "Interval":
                    self.currentIntervalEndTime = columnsAndValues['EndTime']

                if currentTableName == "Event":
                    columnsAndValues['Event_Content'] = element.text

                if self.insertDataIntoDatabase:
                    # Data is intended to be inserted into the database.

                    parseLog = self.processDataToBeInserted(columnsAndValues,
                                                            currentTableName,
                                                            fKeyValue, parseLog,
                                                            pkeyCol)

                if self.debug:
                    print "lastSeqVal = ", self.lastSeqVal

                if self.lastReading(currentTableName, nextTableName):
                    # The last reading set has been reached.

                    if self.debug:
                        print "----- last reading found -----"

                    parseLog += self.logger.logAndWrite(
                        "{%s}" % self.dupeOnInsertCount)
                    parseLog += self.logger.logAndWrite(
                        "[%s]" % self.commitCount)
                    parseLog += self.logger.logAndWrite(
                        "[%s]" % self.elementCount)
                    self.dupeOnInsertCount = 0

                    parseLog += self.logger.logAndWrite("*")
                    self.commitCount += 1
                    self.conn.commit()

                if self.lastRegister(currentTableName, nextTableName):
                    # The last register set has been reached.

                    if self.debug:
                        print "----- last register found -----"

        if self.commitCount == 0:
            parseLog += self.logger.logAndWrite("{%s}" % self.dupeOnInsertCount)
            parseLog += self.logger.logAndWrite("[%s]" % self.commitCount)
            parseLog += self.logger.logAndWrite("[%s]" % self.elementCount)
            self.dupeOnInsertCount = 0

        # Final commit
        parseLog += self.logger.logAndWrite("{%s}" % self.dupeOnInsertCount)
        parseLog += self.logger.logAndWrite("[%s]" % self.commitCount)
        parseLog += self.logger.logAndWrite("[%s]" % self.elementCount)
        self.dupeOnInsertCount = 0

        parseLog += self.logger.logAndWrite("*")
        self.commitCount += 1
        self.conn.commit()
        print

        self.logger.log("Data process count = %s." % self.dataProcessCount, 'info')
        return parseLog


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
        """
        Determine if the last register is being visited.

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
        """
        This is not used.
        """
        self.conn.rollback()
