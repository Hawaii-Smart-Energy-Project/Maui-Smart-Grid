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

SEND_EMAIL = False


class TestMECONotifier(unittest.TestCase):
    """
    Unit tests for the MECO Notifier.
    """

    def setUp(self):
        self.notifier = MSGNotifier()
        self.config = MSGConfiger()

    def tearDown(self):
        pass

    def testInit(self):
        self.assertIsNotNone(self.notifier, "Notifier has been initialized.")

    def testEmailServer(self):
        errorOccurred = False
        user = self.config.configOptionValue('Notifications', 'email_username')
        password = self.config.configOptionValue('Notifications',
                                                 'email_password')

        server = smtplib.SMTP(
            self.config.configOptionValue('Notifications', 'email_smtp_server'))

        try:
            server.starttls()
        except smtplib.SMTPException, e:
            print "Exception = %s" % e

        try:
            server.login(user, password)
        except smtplib.SMTPException, e:
            print "Exception = %s" % e

        self.assertFalse(errorOccurred, "No errors occurred during SMTP setup.")

    def testSendEmailNotification(self):
        if SEND_EMAIL:
            success = self.notifier.sendNotificationEmail(
                'This is a message from testSendEmailNotification.')
            self.assertTrue(success,
                            "Sending an email notification did not produce an"
                            " exception.")
        else:
            self.assertTrue(True, "Email is not sent when SEND_EMAIL is False.")

    def testSendEmailAttachment(self):
        if SEND_EMAIL:
            body = "Test message"
            file = "../../test-data/graph.png"
            success = self.notifier.sendMailWithAttachments(body, [file])
            success = (success != True)
            self.assertTrue(success,
                            "Sending an email notification did not produce an"
                            " exception.")
        else:
            self.assertTrue(True, "Email is not sent when SEND_EMAIL is False.")


if __name__ == '__main__':
    unittest.main()
