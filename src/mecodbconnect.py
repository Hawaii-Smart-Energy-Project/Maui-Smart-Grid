#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'

import psycopg2
import psycopg2.extras
from mecoconfig import MECOConfiger

class MECODBConnector(object) :
    """Connect to the MECO database.
    """

    def __init__(self) :
        """Constructor"""

        self.configer = MECOConfiger()
        self.dbPassword = self.configer.configOptionValue("Database", 'db_password')
        self.dbHost = self.configer.configOptionValue("Database", 'db_host')
        self.dbPort = self.configer.configOptionValue("Database", 'db_port')
        self.dbName = self.configer.configOptionValue("Database", 'db_name')
        self.dbUsername = self.configer.configOptionValue("Database", 'db_username')

        self.conn = self.connectDB()
        self.dictCur = self.conn.cursor(cursor_factory = psycopg2.extras.DictCursor)

    def connectDB(self) :
        """Make the DB connection.
        """

        conn = None

        try :
            conn = psycopg2.connect("dbname='%s' user='%s' host='%s' port='%s' password='%s'" % (
                self.dbName, self.dbUsername, self.dbHost, self.dbPort, self.dbPassword))
        except :
            print "Failed to connect to DB"
            return None
        return conn
