#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'
__copyright__ = 'Copyright (c) 2014, University of Hawaii Smart Energy Project'
__license__ = 'https://raw.github' \
              '.com/Hawaii-Smart-Energy-Project/Maui-Smart-Grid/master/BSD' \
              '-LICENSE.txt'

from msg_logger import MSGLogger
from msg_data_aggregator import MSGDataAggregator
from msg_notifier import MSGNotifier
from msg_db_connector import MSGDBConnector
from msg_db_util import MSGDBUtil


NOTIFICATION_HISTORY_TABLE = "NotificationHistory"
NOTIFICATION_HISTORY_TYPE = 'MSG_DATA_AGGREGATOR'


class NewDataAggregator(object):
    """
    Perform aggregation of new data.
    """

    def __init__(self):
        """
        Constructor.
        """
        self.logger = MSGLogger(__name__, 'DEBUG')
        self.aggregator = MSGDataAggregator()
        self.notifier = MSGNotifier()
        self.rawTypes = ['weather', 'egauge', 'circuit', 'irradiance']
        self.connector = MSGDBConnector()
        self.conn = self.connector.connectDB()
        self.cursor = self.conn.cursor()
        self.dbUtil = MSGDBUtil()


    def lastReportDate(self, notificationType):
        """
        Get the last time a notification was reported.

        :param notificationType: string indicating the type of the
        notification. It is stored in the event history.
        :returns: datetime of last report date.
        """

        cursor = self.cursor()
        sql = """SELECT MAX("notificationTime") FROM "{}" WHERE
        "notificationType" = '{}'""".format(NOTIFICATION_HISTORY_TABLE,
                                            notificationType)

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


    def sendNewDataNotification(self, result, testing = False):
        """
        Sending notification reporting on new data being available since the
        last time new data was reported.

        :param testing: Use testing mode when True.
        """

        lastReportDate = self.lastReportDate(NOTIFICATION_HISTORY_TYPE)

        if not lastReportDate:
            lastReportDate = "never"

        msgBody = '\nNew data has been aggregated in {}.'.format(
            self.connector.dbName)
        msgBody += '\n\n'
        for i in range(len(result)):
            msgBody += 'The new data count for type {} is {} readings.'.format(
                result[i].keys, result[i][result[i].keys][0])
        msgBody += '\n\n'
        msgBody += 'The last report date was %s.' % lastReportDate
        msgBody += '\n\n'
        self.notifier.sendNotificationEmail(msgBody, testing = testing)
        self.saveNotificationTime()


    def saveNotificationTime(self):
        """
        Save the notification event to the notification history.
        """

        cursor = self.cursor()
        sql = """INSERT INTO "{}" ("notificationType", "notificationTime")
        VALUES ('{}', NOW())""".format(NOTIFICATION_HISTORY_TABLE,
                                       NOTIFICATION_HISTORY_TYPE)
        success = self.dbUtil.executeSQL(cursor, sql)
        self.conn.commit()
        if not success:
            # @todo Raise an exception.
            self.logger.log(
                'An error occurred while saving the notification time.')


    def aggregateNewData(self):
        """
        :return:
        """

        msg = 'Aggregating new data.'

        result = map(self.aggregator.aggregateNewData, self.rawTypes)

        self.logger.log('result {}'.format(result))


if __name__ == '__main__':
    aggregator = NewDataAggregator()
    aggregator.aggregateNewData()
