#!/usr/bin/env python3
# ----------------------------------------------------------------------------------------------------------------------
# Inconspicuous Backup Service
#
# Copyright 2016 by Inconspicuous Backup Solutions Dev. Team, Christian Beuschel <chris109@web.de>
#
# This file is part of Inconspicuous Backup Service.
#
# Inconspicuous Backup Service is free software: you can redistribute it and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Inconspicuous Backup Service is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
# even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
# for more details.
#
# You should have received a copy of the GNU General Public License along with Inconspicuous Backup Service. If not,
# see <http://www.gnu.org/licenses/>.
#
# ----------------------------------------------------------------------------------------------------------------------

import smtplib
import weakref
from InconspicuousBackupServiceLib.Report import Report


class EMailSender:

    def __init__(self, report, server, username, password, sender, use_tls=True):
        self._server = server
        self._username = username
        self._password = password
        self._sender = sender
        self._report = weakref.ref(report)
        self._use_tls = use_tls

    def send(self, to, subject, body):
        message = "\r\n".join([
            "From: " + self._sender,
            "To: " + to,
            "Subject: " + subject,
            "",
            body])
        try:
            smtp_connection = smtplib.SMTP(self._server)
            smtp_connection.ehlo()
            if self._use_tls is True:
                smtp_connection.starttls()
            if self._password is not None and self._username is not None:
                smtp_connection.login(self._username, self._password)
            smtp_connection.sendmail(self._sender, [to], message)
            smtp_connection.quit()
        except smtplib.SMTPException as e:
            error_code = getattr(e, "smtp_code", -1)
            error_message = getattr(e, "smtp_error", "No message.")
            message = "Unable to send e-mail (Code: {0}, Message: \"{1}\")".format(error_code, error_message)
            report = self._report()
            report.log_error(message)
