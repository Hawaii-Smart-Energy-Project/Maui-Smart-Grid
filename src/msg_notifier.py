#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'
__copyright__ = 'Copyright (c) 2013, University of Hawaii Smart Energy Project'
__license__ = 'https://raw.github' \
              '.com/Hawaii-Smart-Energy-Project/Maui-Smart-Grid/master/BSD' \
              '-LICENSE.txt'

import smtplib
from datetime import datetime
from msg_configer import MSGConfiger
import sys
import os
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import formatdate
from email import Encoders
from msg_logger import MSGLogger


class MSGNotifier(object):
    """
    Provides notification service functionality for MSG data processing.

    Email settings are stored in the local configuration.
    """

    def __init__(self):
        """
        Constructor.
        """

        self.config = MSGConfiger()
        self.logger = MSGLogger(__name__, 'info')
        self.notificationHeader = "This is a message from the Hawaii Smart " \
                                  "Energy Project MSG Project notification " \
                                  "system.\n\n"

        self.noReplyNotice = """\n\nThis email account is not monitored. No
        replies will originate from this account.\n\nYou are receiving this
        message because you are on the recipient list for notifications for
        the Hawaii Smart Energy Project."""


    def sendNotificationEmail(self, msgBody, testing = False):
        """
        This method is an alternative to the multipart method in
        sendMailWithAttachments.

        :param msgBody: The body of the message to be sent.
        :param testing: True if running in testing mode.
        :returns: True for success, False for an error.
        """

        errorOccurred = False
        user = self.config.configOptionValue('Notifications', 'email_username')
        password = self.config.configOptionValue('Notifications',
                                                 'email_password')
        fromaddr = self.config.configOptionValue('Notifications',
                                                 'email_fromaddr')

        if testing:
            toaddr = self.config.configOptionValue('Notifications',
                                                   'testing_email_recipients')
        else:
            toaddr = self.config.configOptionValue('Notifications',
                                                   'email_recipients')
        server = smtplib.SMTP(
            self.config.configOptionValue('Notifications', 'email_smtp_server'))

        try:
            server.starttls()
        except smtplib.SMTPException as detail:
            errorOccurred = True
            self.logger.log("Exception during SMTP STARTTLS: %s" % detail,
                            'ERROR')

        try:
            server.login(user, password)
        except smtplib.SMTPException as detail:
            errorOccurred = True
            self.logger.log("Exception during SMTP login: %s" % detail, 'ERROR')

        senddate = datetime.strftime(datetime.now(), '%Y-%m-%d')
        subject = "HISEP Notification"

        msgHeader = "Date: %s\r\nFrom: %s\r\nTo: %s\r\nSubject: " \
                    "%s\r\nX-Mailer: " \
                    "My-Mail\r\n\r\n" % (
                        senddate, fromaddr, toaddr, subject)

        msgBody = self.notificationHeader + msgBody

        msgBody += self.noReplyNotice

        try:
            self.logger.log("Send email notification.", 'INFO')
            server.sendmail(fromaddr, toaddr, msgHeader + msgBody)
            server.quit()
        except smtplib.SMTPException as detail:
            errorOccurred = True
            self.logger.log("Exception during SMTP sendmail: %s" % detail,
                            'ERROR')

        return errorOccurred != True


    def sendMailWithAttachments(self, msgBody, files = None, testing = False):
        """
        Send email along with attachments.

        :param msgBody: String containing the body of the messsage to send.
        :param files: List of file paths. This is a mutable argument that
        should be handled carefully as the default is defined only once.
        :param testing: True if running in testing mode.
        :returns: True if no exceptions are raised.
        """

        if files is None:
            files = []

        sys.stderr.write("Sending multipart email.\n")
        if testing:
            self.logger.log("Notification testing mode is ON.\n", 'info')

        errorOccurred = False
        assert type(files) == list

        user = self.config.configOptionValue('Notifications', 'email_username')
        password = self.config.configOptionValue('Notifications',
                                                 'email_password')

        if testing:
            send_to = self.config.configOptionValue('Notifications',
                                                    'testing_email_recipients')
        else:
            send_to = self.config.configOptionValue('Notifications',
                                                    'email_recipients')

        send_from = self.config.configOptionValue('Notifications',
                                                  'email_fromaddr')

        msg = MIMEMultipart()
        msg['From'] = send_from
        msg['To'] = send_to
        msg['Date'] = formatdate(localtime = True)
        msg['Subject'] = "HISEP Notification"

        msg.attach(MIMEText(msgBody))

        for f in files:
            sys.stderr.write("Attaching file %s.\n" % f)
            part = MIMEBase('application', "octet-stream")
            part.set_payload(open(f, "rb").read())
            Encoders.encode_base64(part)
            part.add_header('Content-Disposition',
                            'attachment; filename="%s"' % os.path.basename(f))
            msg.attach(part)

        server = smtplib.SMTP(
            self.config.configOptionValue('Notifications', 'email_smtp_server'))
        try:
            server.starttls()
        except smtplib.SMTPException as detail:
            errorOccurred = True
            self.logger.log("Exception during SMTP STARTTLS: %s" % detail,
                            'ERROR')

        try:
            server.login(user, password)
        except smtplib.SMTPException as detail:
            errorOccurred = True
            self.logger.log("Exception during SMTP login: %s" % detail, 'ERROR')

        self.logger.log("Send email notification.", 'INFO')

        try:
            server.sendmail(send_from, send_to, msg.as_string())
        except smtplib.SMTPException as detail:
            errorOccurred = True
            self.logger.log("Exception during SMTP sendmail: %s" % detail,
                            'ERROR')

        server.quit()

        if errorOccurred == False:
            self.logger.log('No exceptions occurred.\n', 'info')

        return errorOccurred
