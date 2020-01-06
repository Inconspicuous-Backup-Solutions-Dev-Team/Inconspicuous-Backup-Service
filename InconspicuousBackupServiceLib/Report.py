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

import datetime
import os

# Functions
# ----------------------------------------------------------------------------------------------------------------------


def html_format_document_header(title):
    headline = title.replace("\n", "<br>")
    title = title.replace("\n", " ")
    return ('<!DOCTYPE html>\n'
            '<html lang="en">\n'
            '<head>\n'
            '    <meta charset="utf-8">\n'
            '    <title>{0}</title>\n'
            '    <meta name="description" content="Backup Report">\n'
            '    <meta name="author" content="Inconspicuous Backup Service">\n'
            '    <link rel="stylesheet" href="backup-report-stylesheet.css">\n'
            '</head>\n'
            '<body>\n'
            '<div class="position">\n'
            '<div class="report">\n'
            '<h1>{1}</h1>\n').format(title, headline)


def html_format_section_host_header():
    return ("<h2>Host cloning summary</h2>\n"
            "<div class=\"summary\">\n")


def html_format_host_summary_line(host_info, summary, runtime_info):
    summary_string = ""
    summary_css_class = ""
    if summary == Report.LOG_SUMMARY_SUCCESS:
        summary_css_class = "success"
        summary_string = "SUCCESS"
    elif summary == Report.LOG_SUMMARY_WARN:
        summary_css_class = "warn"
        summary_string = "WARN"
    elif summary == Report.LOG_SUMMARY_FAIL:
        summary_css_class = "fail"
        summary_string = "FAIL"
    return ("<div class=\"summary_line\">\n"
            "    <div class=\"summary_cell_host\">\n"
            "        {0}\n"
            "    </div>\n"
            "    <div class=\"summary_cell_result {1}\">\n"
            "        {2}\n"
            "    </div>\n"
            "    <div class=\"summary_cell_runtime_data\">\n"
            "        {3}\n"
            "    </div>\n"
            "</div>").format(host_info, summary_css_class, summary_string, runtime_info)


def html_format_section_host_footer():
    return "</div>\n"


def html_format_section_job_header():
    return ("<h2>Backup Job Summary</h2>\n"
            "<div class=\"summary\">\n")


def html_format_job_summary_line(job_info, summary, runtime_info):
    summary_string = ""
    summary_css_class = ""
    if summary == Report.LOG_SUMMARY_SUCCESS:
        summary_css_class = "success"
        summary_string = "SUCCESS"
    elif summary == Report.LOG_SUMMARY_WARN:
        summary_css_class = "warn"
        summary_string = "WARN"
    elif summary == Report.LOG_SUMMARY_FAIL:
        summary_css_class = "fail"
        summary_string = "FAIL"
    return ("<div class=\"summary_line\">\n"
            "    <div class=\"summary_cell_job\">\n"
            "        {0}\n"
            "    </div>\n"
            "    <div class=\"summary_cell_result {1}\">\n"
            "        {2}\n"
            "    </div>\n"
            "    <div class=\"summary_cell_runtime_data\">\n"
            "        {3}\n"
            "    </div>\n"
            "</div>").format(job_info, summary_css_class, summary_string, runtime_info)


def html_format_section_job_footer():
    return "</div>\n"


def html_format_section_linear_log_header():
    return ("<h2>Linear Log</h2>\n"
            "<div class=\"summary\">\n")


def html_format_linear_log_entry(timestamp, log_level, message):
    timestamp_string = timestamp.strftime("%Y-%m-%d %H:%M:%S")
    log_level_css_class = ""
    log_level_string = ""
    if log_level == Report.LOG_LEVEL_INFO:
        log_level_css_class = "info"
        log_level_string = "INFO"
    elif log_level == Report.LOG_LEVEL_WARN:
        log_level_css_class = "warn"
        log_level_string = "WARN"
    elif log_level == Report.LOG_LEVEL_ERROR:
        log_level_css_class = "error"
        log_level_string = "ERROR"
    return ("<div class=\"log_line\">\n"
            "    <div class=\"log_timestamp\">\n"
            "        {0}\n"
            "    </div>\n"
            "    <div class=\"log_level {1}\">\n"
            "        {2}\n"
            "    </div>\n"
            "    <div class=\"log_message\">\n"
            "        {3}\n"
            "    </div>\n"
            "</div>\n").format(timestamp_string, log_level_css_class, log_level_string, message)


def html_format_section_linear_log_footer():
    return "</div>\n"


def html_format_document_footer():
    return ("</div>\n"
            "</div>\n"
            "</body>\n"
            "</html>")

# Class: Report
# ----------------------------------------------------------------------------------------------------------------------


class Report:

    LOG_LEVEL_INFO = "INFO"
    LOG_LEVEL_WARN = "WARN"
    LOG_LEVEL_ERROR = "ERROR"

    LOG_SUMMARY_SUCCESS = "SUCCESS"
    LOG_SUMMARY_WARN = "WARN"
    LOG_SUMMARY_FAIL = "FAIL"

    def __init__(self):
        self._directory = None
        self._file_name = None
        self._file = None
        self._email_configuration = None
        self._title = ""
        self._linear_log = []
        self._host_summary_log = {}
        self._job_summary_log = {}

    def configure(self, directory, title, filename, email_configuration):
        self._directory = directory
        self._file_name = filename
        self._title = title
        self._email_configuration = email_configuration

    def log(self, log_level, message):
        timestamp = datetime.datetime.now()
        log_entry = LinearLogItem(timestamp, log_level, message)
        self._linear_log.append(log_entry)
        log_entry.print_to_terminal()

    def log_error(self, message):
        self.log(self.LOG_LEVEL_ERROR, message)

    def log_warn(self, message):
        self.log(self.LOG_LEVEL_WARN, message)

    def log_info(self, message):
        self.log(self.LOG_LEVEL_INFO, message)

    def set_host_summary(self, host_identification_string, hostname=None, summary=None, details=None):
        try:
            summary_entry = self._host_summary_log[host_identification_string]
        except KeyError:
            summary_entry = HostSummaryItem(host_identification_string)
        if summary is not None:
            if summary == self.LOG_SUMMARY_WARN:
                if summary_entry.summary == self.LOG_SUMMARY_FAIL:
                    summary = self.LOG_SUMMARY_FAIL
            elif summary == self.LOG_SUMMARY_SUCCESS:
                if summary_entry.summary == self.LOG_SUMMARY_FAIL:
                    summary = self.LOG_SUMMARY_FAIL
                elif summary_entry.summary == self.LOG_SUMMARY_WARN:
                    summary = self.LOG_SUMMARY_WARN
        summary_entry.host_name = hostname if hostname is not None else summary_entry.host_name
        summary_entry.summary = summary if summary is not None else summary_entry.summary
        summary_entry.details = details if details is not None else summary_entry.details
        self._host_summary_log[host_identification_string] = summary_entry

    def set_job_summary(self, job_id_string, description=None, summary=None, details=None):
        try:
            summary_entry = self._job_summary_log[job_id_string]
        except KeyError:
            summary_entry = JobSummaryItem(job_id_string)
        if summary is not None:
            if summary == self.LOG_SUMMARY_WARN:
                if summary_entry.summary == self.LOG_SUMMARY_FAIL:
                    summary = self.LOG_SUMMARY_FAIL
            elif summary == self.LOG_SUMMARY_SUCCESS:
                if summary_entry.summary == self.LOG_SUMMARY_FAIL:
                    summary = self.LOG_SUMMARY_FAIL
                elif summary_entry.summary == self.LOG_SUMMARY_WARN:
                    summary = self.LOG_SUMMARY_WARN
        summary_entry.description = description if description is not None else summary_entry.description
        summary_entry.summary = summary if summary is not None else summary_entry.summary
        summary_entry.details = details if details is not None else summary_entry.details
        self._job_summary_log[job_id_string] = summary_entry

    def write_html_file(self):
        file_path = os.path.join(self._directory, self._file_name)
        with open(file_path, 'w') as f:
            f.write(html_format_document_header(self._title))

            f.write(html_format_section_host_header())
            for host_summary in self._host_summary_log.values():
                f.write(host_summary.get_html())
            f.write(html_format_section_host_footer())

            f.write(html_format_section_job_header())
            for job_summary in self._job_summary_log.values():
                f.write(job_summary.get_html())
            f.write(html_format_section_job_footer())

            f.write(html_format_section_linear_log_header())
            for log_entry in self._linear_log:
                f.write(log_entry.get_html())
            f.write(html_format_section_linear_log_footer())
    def send_mail(self):
        pass


# Class: LinearLogEntry
# ----------------------------------------------------------------------------------------------------------------------

class LinearLogItem:

    def __init__(self, timestamp, log_level, message):
        self._timestamp = timestamp
        self._log_level = log_level
        self._message = message

    def get_html(self):
        return html_format_linear_log_entry(self._timestamp, self._log_level, self._message)

    def print_to_terminal(self):
        time_sting = self._timestamp.strftime("%Y-%m-%d %a. %H:%M:%S")
        level_string = self._log_level
        print("{0} - {1} : {2}".format(time_sting, level_string, self._message))


# Class: HostSummaryEntry
# ----------------------------------------------------------------------------------------------------------------------


class HostSummaryItem:

    identification_string = None
    host_name = ""
    summary = Report.LOG_SUMMARY_SUCCESS
    details = ""

    def __init__(self, id_string):
        self.identification_string = id_string

    def get_html(self):
        return html_format_host_summary_line("{0}: {1}".format(self.identification_string, self.host_name),
                                             self.summary,
                                             self.details)


class JobSummaryItem:

    identification_string = None
    description = ""
    summary = Report.LOG_SUMMARY_SUCCESS
    details = ""

    def __init__(self, id_string):
        self.identification_string = id_string

    def get_html(self):
        return html_format_job_summary_line("{0}: {1}".format(self.identification_string, self.description),
                                            self.summary,
                                            self.details)
