#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@todo Separate the script and the class.
"""

__author__ = 'Daniel Zhang (張道博)'
__copyright__ = 'Copyright (c) 2013, University of Hawaii Smart Energy Project'
__license__ = 'https://raw.github' \
              '.com/Hawaii-Smart-Energy-Project/Maui-Smart-Grid/master/BSD' \
              '-LICENSE.txt'

from msg_db_connector import MSGDBConnector
from msg_db_util import MSGDBUtil
from msg_configer import MSGConfiger
from msg_notifier import MSGNotifier
from msg_logger import MSGLogger
from datetime import datetime as dt


NOTIFICATION_HISTORY_TABLE = "NotificationHistory"


class MSGEgaugeNewDataChecker(object):
    """
    Provide notification of newly loaded MSG eGauge data.

    This uses notification type MSG_EGAUGE_SERVICE.
    """

    def __init__(self):
        """
        Constructor.
        """

        print __name__
        self.logger = MSGLogger(__name__)
        self.connector = MSGDBConnector()
        self.dbUtil = MSGDBUtil()
        self.notifier = MSGNotifier()
        self.configer = MSGConfiger()


    def newDataCount(self):
        """
        Measure the amount of new data that is present since the last time
        new data was reported.
        """

        cursor = self.connector.conn.cursor()
        tableName = 'EgaugeEnergyAutoload'
        lastTime = self.lastReportDate('MSG_EGAUGE_SERVICE')
        if lastTime is None:
            lastTime = '1900-01-01'
        sql = """SELECT COUNT(*) FROM "%s" WHERE datetime > '%s'""" % (
            tableName, lastTime)

        success = self.dbUtil.executeSQL(cursor, sql)
        if success:
            rows = cursor.fetchall()

            if not rows[0][0]:
                return 0
            else:
                return rows[0][0]
        else:
            # @todo Raise an exception.
            return None


    def lastReportDate(self, notificationType):
        """
        Get the last time a notification was reported.

        :param notificationType: A string indicating the type of the notification. It is stored in the event history.
        :returns: datetime of last report date.
        """

        cursor = self.connector.conn.cursor()
        sql = """SELECT MAX("notificationTime") FROM "%s" WHERE
        "notificationType" = '%s'""" % (
            NOTIFICATION_HISTORY_TABLE, notificationType)

        success = self.dbUtil.executeSQL(cursor, sql)
        if success:
            rows = cursor.fetchall()

            if not rows[0][0]:
                return None
            else:
                return rows[0][0]
        else:
            # @todo Raise an exception.
            return None


    def saveNotificationTime(self):
        """
        Save the notification event to the notification history.
        """

        cursor = self.connector.conn.cursor()
        sql = """INSERT INTO "%s" ("notificationType", "notificationTime")
        VALUES ('MSG_EGAUGE_SERVICE', NOW())""" % NOTIFICATION_HISTORY_TABLE
        success = self.dbUtil.executeSQL(cursor, sql)
        self.connector.conn.commit()
        if not success:
            # @todo Raise an exception.
            self.logger.log(
                'An error occurred while saving the notification time.')


    def sendNewDataNotification(self, testing = False):
        """
        Sending notification reporting on new data being available since the
        last time new data was reported.

        :param testing: Use testing mode flag.
        """

        lastReportDate = self.lastReportDate('MSG_EGAUGE_SERVICE')

        if not lastReportDate:
            lastReportDate = "never"

        msgBody = '\nNew MSG eGauge data has been loaded to %s.' % self \
            .connector.dbName
        msgBody += '\n\n'
        msgBody += 'The new data count is %s readings.' % self.newDataCount()
        msgBody += '\n\n'
        msgBody += 'The last report date was %s.' % lastReportDate
        msgBody += '\n\n'
        self.notifier.sendNotificationEmail(msgBody, testing = testing)
        self.saveNotificationTime()


if __name__ == '__main__':

    checker = MSGEgaugeNewDataChecker()
    checker.sendNewDataNotification()
