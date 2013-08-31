#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'
__copyright__ = 'Copyright (c) 2013, University of Hawaii Smart Energy Project'
__license__ = 'https://raw.github' \
              '.com/Hawaii-Smart-Energy-Project/Maui-Smart-Grid/master/BSD' \
              '-LICENSE.txt'

from msg_db_connector import MSGDBConnector
from msg_configer import MSGConfiger
from msg_notifier import MSGNotifier
from msg_logger import MSGLogger


class MSGEguageNewDataChecker(object):
    """
    Provide notification of newly loaded data.

    This uses notification type MSG_EGAUGE.
    """

    def __init__(self):
        """
        Constructor.
        """

        self.logger = MSGLogger(__name__)
        self.connector = MSGDBConnector()
        self.notifier = MSGNotifier()
        self.configer = MSGConfiger()


    def newDataCount(self):
        """
        Measure the amount of new data that is present since the last time new data was reported.
        """

        tableName = 'EgaugeEnergyAutoload'
        sql = """SELECT COUNT(*) FROM %s WHERE datetime > %s""" % (tableName, self.lastReportDate())


    def lastReportDate(self):
        """
        Get the last time a notification was reported.
        """

        sql = """SELECT MAX(notificationTime) FROM NotificationHistory WHERE notificationType = 'MSG_EGAUGE'"""


    def sendNewDataNotification(self):
        """
        Sending notification reporting on new data being available since the last time new data was reported.
        """

        dbName = ''
        msgBody = 'New MSG eGauge data has been loaded to %s.' % dbName
        msgBody += ''
        self.notifier.sendNotificationEmail(self, msgBody, testing = False)
