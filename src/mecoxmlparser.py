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

INSERT_DATA = 0
DEBUG = 1

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

        self.filename=None
        self.elementCount = 0
        self.inserter = MECODBInserter()

        # count how many times sections in source data are encountered
        self.tableNameCount = {'SSNExportDocument' : 0, 'MeterData' : 0, 'RegisterData' : 0,
                               'RegisterRead' : 0, 'Tier' : 0, 'Register' : 0,
                               'IntervalReadData' : 0, 'Interval' : 0, 'Reading' : 0,
                               'IntervalStatus' : 0, 'ChannelStatus' : 0}

        self.insertTables = self.mecoConfig.insertTables

        self.lastSeqVal = None
        self.fKeyVal = None
        self.lastTable = None
        self.fkDeterminer = MECOFKDeterminer()

    def parseXML(self) :
        """Parse an XML file.
        """

        print "parsing xml in", self.filename
        tree = ET.parse(self.filename)
        root = tree.getroot()
        self.walkTheTreeFromRoot(root)

    def walkTheTreeFromRoot(self, root) :
        """Walk an XML tree from its root node.
        :param root Root node of an XML tree.
        """

        walker = root.iter()
        for element in walker :
            self.elementCount += 1

            tableName = re.search('\{.*\}(.*)', element.tag).group(1) # current table name

            self.tableNameCount[tableName] += 1

            columnsAndValues = {}
            it = iter(sorted(element.attrib.iteritems()))

            for item in list(it) :
                # Create a dictionary of column names and values.
                columnsAndValues[item[0]] = item[1]

            if tableName in self.insertTables :
                if DEBUG :
                    print
                    print "processing table %s" % tableName
                    print "--------------------------------"

                pkeyCol = self.mapper.dbColumnsForTable(tableName)[
                          '_pkey'] # get the col name for the pkey
                fkeyCol = None
                fKeyValue = None

                try :
                    fkeyCol = self.mapper.dbColumnsForTable(tableName)[
                              '_fkey'] # get the col name for the fkey
                except :
                    pass

                if DEBUG :
                    print "foreign key col (fkey) = %s" % fkeyCol
                    print "primary key col (pkey) = %s" % pkeyCol
                    print columnsAndValues

                # get fk value
                if fkeyCol is not None :
                    fKeyValue = self.fkDeterminer.pkValforCol[fkeyCol]

                if DEBUG :
                    print "fKeyValue = %s" % fKeyValue

                cur = self.inserter.insertData(self.conn, tableName, columnsAndValues, fKeyValue, 1)

                self.lastSeqVal = self.util.getLastSequenceID(self.conn, tableName,
                                                              pkeyCol)
                # store pk
                self.fkDeterminer.pkValforCol[pkeyCol] = self.lastSeqVal

                if DEBUG :
                    print "lastSeqVal = ", self.lastSeqVal

            if self.elementCount % 10000 == 0:
                sys.stdout.write('.')
                self.conn.commit()
        print
