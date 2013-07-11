#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'

import psycopg2
import psycopg2.extras
from msg_config import MSGConfiger
from msg_logger import MSGLogger


class MECODBConnector(object):
    """
    Manage a connection to a MECO database.
    """

    def __init__(self, testing = False, logLevel = 'silent'):
        """
        Constructor.

        :param testing: Boolean indicating if Testing Mode is on.
        :param logLevel
        """

        self.logger = MSGLogger(__name__, logLevel)

        if (testing):
            self.logger.log("Testing Mode is ON.")

        self.configer = MSGConfiger()
        self.dbPassword = self.configer.configOptionValue("Database",
                                                          'db_password')
        self.dbHost = self.configer.configOptionValue("Database", 'db_host')
        self.dbPort = self.configer.configOptionValue("Database", 'db_port')

        if testing:
            self.dbName = self.configer.configOptionValue("Database",
                                                          'testing_db_name')
        else:
            self.dbName = self.configer.configOptionValue("Database", 'db_name')

        self.logger.log(
            "Instantiating DB connector with database %s." % self.dbName)

        self.dbUsername = self.configer.configOptionValue("Database",
                                                          'db_username')

        self.conn = self.connectDB()
        self.dictCur = self.conn.cursor(
            cursor_factory = psycopg2.extras.DictCursor)


    def connectDB(self):
        """
        Make the DB connection.
        """

        conn = None

        try:
            conn = psycopg2.connect(
                "dbname='%s' user='%s' host='%s' port='%s' password='%s'" % (
                    self.dbName, self.dbUsername, self.dbHost, self.dbPort,
                    self.dbPassword))
        except:
            self.logger.log("Failed to connect to the database.", 'error')
            return None

        self.logger.log("Opened DB connection to database %s." % self.dbName)
        return conn

    def closeDB(self, conn):
        """
        Close a database connection.
        """

        self.logger.log("Closing database %s." % self.dbName)
        conn.close()

    def __del__(self):
        """
        Destructor.

        Close the database connection.
        """

        import sys

        self.logger.log(
            "Closing the DB connection to database %s." % self.dbName)
        self.conn.close()

