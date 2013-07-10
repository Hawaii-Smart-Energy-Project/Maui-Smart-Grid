#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'

from msg_logger import MSGLogger
from mecodbutils import MECODBUtil

class MSGWeatherDataDupeChecker(object):
    """
    Determine if a duplicate record exists based on the tuple

    (WBAN, Date, Time, StationType).
    """

    def __init__(self,testing=False):
        """
        Constructor.
        """

        self.logger = MSGLogger(__name__, 'debug')
        self.dbUtil = MECODBUtil()


    def duplicateExists(self, dbCursor, wban, datetime, recordType):
        """
        Check for the existence of a duplicate record.

        :param dbCursor
        :param wban
        :param datetime
        :param recordType
        :returns: True if a duplicate record exists, otherwise False.
        """

        tableName = "WeatherNOAA"
        sql = """SELECT wban, datetime, record_type FROM \"%s\" WHERE
                 wban = '%s' AND datetime = '%s' AND record_type = '%s'""" % (
            tableName, wban, datetime, recordType)

        self.logger.log("sql=%s" % sql, 'debug')
        self.logger.log("wban=%s, datetime=%s, record_type=%s" % (
        wban, datetime, recordType), 'debug')

        self.dbUtil.executeSQL(dbCursor, sql)
        rows = dbCursor.fetchall()

        if len(rows) > 0:
            return True
        else:
            return False
