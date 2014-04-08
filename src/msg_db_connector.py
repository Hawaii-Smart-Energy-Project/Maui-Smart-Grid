#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'
__copyright__ = 'Copyright (c) 2014, University of Hawaii Smart Energy Project'
__license__ = 'https://raw.github' \
              '.com/Hawaii-Smart-Energy-Project/Maui-Smart-Grid/master/BSD' \
              '-LICENSE.txt'

import psycopg2
import psycopg2.extras
from msg_configer import MSGConfiger
from msg_logger import MSGLogger


class MSGDBConnector(object):
    """
    Manage a connection to an MSG database.

    Usage:

        conn = MSGDBConnector().connectDB()
        cursor = self.conn.cursor()

    """

    def __init__(self, testing = False, logLevel = 'silent'):
        """
        Constructor.

        :param testing: Boolean indicating if Testing Mode is on. When
        testing mode is on, a connection to the testing database will be made
        instead of the production database. This is useful for unit testing.
        :param logLevel
        """

        self.logger = MSGLogger(__name__, logLevel)

        if testing:
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
            "Instantiating DB connector with database {}.".format(self.dbName))

        self.dbUsername = self.configer.configOptionValue("Database",
                                                          'db_username')

        self.conn = self.connectDB()
        if not self.conn:
            raise Exception('DB connection not available.')

        try:
            self.dictCur = self.conn.cursor(
                cursor_factory = psycopg2.extras.DictCursor)
        except AttributeError as error:
            self.logger.log('Error while getting DictCursor: {}'.format(error))


    def connectDB(self):
        """
        Make the DB connection.
        :returns: DB connection object if successful, otherwise None.
        """

        # @todo Make this method private since the init makes the connection.

        conn = None

        try:
            conn = psycopg2.connect(
                "dbname='{0}' user='{1}' host='{2}' port='{3}' password='{"
                "4}'".format(self.dbName, self.dbUsername, self.dbHost,
                             self.dbPort, self.dbPassword))
        except:
            self.logger.log("Failed to connect to the database.", 'error')
            return None

        self.logger.log(
            "Opened DB connection to database {}.".format(self.dbName))
        return conn

    def closeDB(self, conn):
        """
        Close a database connection.
        """

        self.logger.log("Closing database {}.".format(self.dbName))
        conn.close()

    def __del__(self):
        """
        Destructor.

        Close the database connection.
        """

        import sys

        self.logger.log(
            "Closing the DB connection to database {}.".format(self.dbName))
        self.conn.close()

