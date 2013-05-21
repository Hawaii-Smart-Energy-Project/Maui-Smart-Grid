#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'

import psycopg2
import psycopg2.extras
from mecoconfig import MECOConfiger
import sys

class MECODBConnector(object) :
    """
    Manage a connection to a MECO database.
    """

    def __init__(self, testing=False) :
        """
        Constructor.

        :param testing: Boolean indicating if Testing Mode is on.
        """

        if(testing):
            print "Testing Mode is ON."

        self.configer = MECOConfiger()
        self.dbPassword = self.configer.configOptionValue("Database", 'db_password')
        self.dbHost = self.configer.configOptionValue("Database", 'db_host')
        self.dbPort = self.configer.configOptionValue("Database", 'db_port')

        if testing:
            self.dbName = self.configer.configOptionValue("Database", 'testing_db_name')
        else:
            self.dbName = self.configer.configOptionValue("Database", 'db_name')

        print "Using database %s." % self.dbName

        self.dbUsername = self.configer.configOptionValue("Database", 'db_username')

        self.conn = self.connectDB()
        self.dictCur = self.conn.cursor(cursor_factory = psycopg2.extras.DictCursor)

    def connectDB(self) :
        """
        Make the DB connection.
        """

        conn = None

        try :
            conn = psycopg2.connect("dbname='%s' user='%s' host='%s' port='%s' password='%s'" % (
                self.dbName, self.dbUsername, self.dbHost, self.dbPort, self.dbPassword))
        except :
            print "Failed to connect to the database."
            return None
        return conn

    def closeDB(self, conn):
        """
        Close a database connection.
        """

        print "Closing database %s." % self.dbName
        conn.close()

    def __del__(self):
        """
        Destructor.

        Close the database connection.
        """

        sys.stderr.write("\nClosing the DB connection to %s.\n" % self.dbName)
        self.conn.close()

