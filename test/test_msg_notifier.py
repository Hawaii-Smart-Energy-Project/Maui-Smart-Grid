#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'
__copyright__ = 'Copyright (c) 2013, University of Hawaii Smart Energy Project'
__license__ = 'https://raw.github' \
              '.com/Hawaii-Smart-Energy-Project/Maui-Smart-Grid/master/BSD' \
              '-LICENSE.txt'

import unittest
from msg_notifier import MSGNotifier
import smtplib
from msg_configer import MSGConfiger
from msg_logger import MSGLogger
import os

SEND_EMAIL = False


class TestMECONotifier(unittest.TestCase):
    """
    Unit tests for the MECO Notifier.
    """

    def setUp(self):
        self.logger = MSGLogger(__name__)
        self.notifier = MSGNotifier()
        self.configer = MSGConfiger()

    def tearDown(self):
        pass

    def testInit(self):
        self.assertIsNotNone(self.notifier, "Notifier has been initialized.")


    def testEmailServer(self):
        """
        Test connecting to the email server.
        """

        errorOccurred = False
        user = self.configer.configOptionValue('Notifications',
                                               'email_username')
        password = self.configer.configOptionValue('Notifications',
                                                   'email_password')

        server = smtplib.SMTP(self.configer.configOptionValue('Notifications',
                                                              'smtp_server_and_port'))

        try:
            server.starttls()
        except smtplib.SMTPException as detail:
            self.logger.log("Exception: {}".format(detail))

        try:
            server.login(user, password)
        except smtplib.SMTPException as detail:
            self.logger.log("Exception: {}".format(detail))

        self.assertFalse(errorOccurred, "No errors occurred during SMTP setup.")


    def testSendEmailNotification(self):
        """
        Send a test notification by email.
        """

        if SEND_EMAIL:
            success = self.notifier.sendNotificationEmail(
                'This is a message from testSendEmailNotification.',
                testing = True)
            self.assertTrue(success,
                            "Sending an email notification did not produce an"
                            " exception.")
        else:
            self.assertTrue(True, "Email is not sent when SEND_EMAIL is False.")


    def testSendEmailAttachment(self):
        """
        Send a test notification with attachment by email.
        """

        if SEND_EMAIL:
            body = "Test message"
            testDataPath = self.configer.configOptionValue('Testing',
                                                           'test_data_path')
            file = os.path.join(testDataPath, 'graph.png')
            success = self.notifier.sendMailWithAttachments(body, [file],
                                                            testing = True)
            success = (success != True)
            self.assertTrue(success,
                            "Sending an email notification did not produce an"
                            " exception.")
        else:
            self.assertTrue(True, "Email is not sent when SEND_EMAIL is False.")


if __name__ == '__main__':
    unittest.main()
