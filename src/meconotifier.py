#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'

import smtplib
from datetime import datetime
from mecoconfig import MECOConfiger


class MECONotifier(object):
    """
    Notification services for MECO data processing.
    """

    def __init__(self):
        """
        Constructor.
        """

        self.config = MECOConfiger()

    def sendNotificationEmail(self, msgBody):
        """
        :param msgBody: The body of the message to be sent.
        :returns: True for success, False for an error.
        """

        errorOccurred = False
        user = self.config.configOptionValue('Notifications', 'email_username')
        password = self.config.configOptionValue('Notifications',
                                                 'email_password')
        fromaddr = self.config.configOptionValue('Notifications',
                                                 'email_fromaddr')
        toaddr = self.config.configOptionValue('Notifications',
                                               'email_recipients')
        server = smtplib.SMTP(
            self.config.configOptionValue('Notifications', 'email_smtp_server'))

        try:
            server.starttls()
        except smtplib.SMTPException, e:
            errorOccurred = True
            print "Exception = %s" % e

        try:
            server.login(user, password)
        except smtplib.SMTPException, e:
            errorOccurred = True
            print "Exception = %s" % e

        senddate = datetime.strftime(datetime.now(), '%Y-%m-%d')
        subject = "Email Test Send"

        msgHeader = "Date: %s\r\nFrom: %s\r\nTo: %s\r\nSubject: " \
                    "%s\r\nX-Mailer: " \
                    "My-Mail\r\n\r\n" % (
                        senddate, fromaddr, toaddr, subject)
        msgBody += '\n\nThis email account is not monitored so don\'t send ' \
                   'messages to it with the expectation of a reply.'

        try:
            server.sendmail(fromaddr, toaddr, msgHeader + msgBody)
            server.quit()
        except smtplib.SMTPException, e:
            errorOccurred = True
            print "Exception = %s" % e

        return errorOccurred != True
