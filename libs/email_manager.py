from getpass import getpass
from os.path import exists, isfile
from libs.finished_manager import FinishedLabHandler
import smtplib
from os.path import basename
from traceback import print_exc
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import json

__author__ = "Joshua D. Katz"


class EmailManager:
    def __init__(self, grader_ucid, password, course, section):
        """
        Create an EmailManager for a grader by UCID and password.

        :param grader_ucid: The grader's UCID.
        :param password: The password for the grader's email.
        :param course: The course that is being graded.
        :param section: The section that is being grader.
        :return:
        """
        self.grader_ucid = grader_ucid
        self.password = password
        self.course = course
        self.section = section
        self.connection = None

    @staticmethod
    def get_email_address(ucid):
        """
        Get an email address for a UCID.

        :param ucid: The UCID to get an email address for.
        :return: ucid + "@njit.edu"
        """
        return "%s@njit.edu" % ucid

    def get_smtp_connection(self):
        """
        Get the SMTP connection for the EmailManager.

        :return: an instance of smtplib.SMTP
        """
        if self.connection is None:
            self.connection = smtplib.SMTP("smtp.gmail.com:587")
            self.connection.starttls()
            self.connection.login(self.get_email_address(self.grader_ucid), self.password)
        return self.connection

    def close_smtp_connection(self):
        """
        Close the SMTP connection.

        :return:
        """
        if self.connection is not None:
            self.connection.quit()
        self.connection = None

    def create_mime_multipart_email_to(self, receiver_ucid, message, subject, attachments=None):
        """
        Create a mutli-part email message.

        :param receiver_ucid: The UCID to send to.
        :param message: The message to send to receiver.
        :param subject: The subject of the email.
        :param attachments: None or a list of strings, file handles, or tuples with (name, content) to be attachments.
        :return: An instance of MIMEMultipart message filled with the data passed.
        """
        email = MIMEMultipart()

        email["From"] = self.get_email_address(self.grader_ucid)
        email["To"] = self.get_email_address(receiver_ucid)
        email["Subject"] = subject
        email.attach(MIMEText(message, "plain"))

        if attachments:

            generated_attachment_number = 0

            for attachment in attachments:

                part = MIMEBase("application", "octet-stream")

                if type(attachment) is tuple:
                    payload = attachment[1].encode("utf8")
                    filename = attachment[0]
                elif type(attachment) is str:
                    payload = attachment.encode("utf8")
                    if generated_attachment_number == 0:
                        filename = "attachment.txt"
                    else:
                        filename = "attachment.%d.txt" % generated_attachment_number
                    generated_attachment_number += 1
                else:
                    payload = attachment.read()
                    filename = basename(attachment.name)

                part.set_payload(payload)
                encoders.encode_base64(part)
                part.add_header("Content-Disposition", "attachment; filename=%s" % filename)

                email.attach(part)

        return email

    def send_email(self, ucid, message, subject=None, attachments=None):
        """
        Send an email to a person by UCID.

        :param ucid: The UCID to send the email to.
        :param message: The message to send to the ucid.
        :param subject: The subject to be set. Generated if not set.
        :param attachments: Attachments for the email, None if nothing to attach.
        :return:
        """
        try:

            connection = self.get_smtp_connection()

            if subject is None:
                subject = "%s-%s email from %s" % (self.course, self.section, self.grader_ucid)

            email = self.create_mime_multipart_email_to(ucid, message, subject, attachments)

            connection.sendmail(email["From"], email["To"], email.as_string())

        except smtplib.SMTPAuthenticationError:
            print("Error connection to SMTP.")
            print_exc()


class EmailDispatcher(FinishedLabHandler):
    def __init__(self, enable_email, email_default, preferences_path, course, section):
        """
        Initialize an email dispatcher object. This will collect the login info for the grader UCID.

        :param enable_email: If email should be enabled.
        :param email_default: The default setting to use for email.
        :param preferences_path: The path to the preferences for files for student email preferences.
        :param course: The course that the AutoGrader is grading for.
        :param section: The section that the AutoGrader is grading for.
        :return:
        """
        self.enable_email = enable_email
        self.email_default = email_default
        self.course = course
        self.section = section

        if not exists(preferences_path) or not isfile(preferences_path):
            self.enable_email = email_default == "ALWAYS"
            print("No email dispatch preferences found at %s." % preferences_path)
            if self.enable_email:
                print("You ALWAYS send by default. Email has been enabled and will send to everyone.")
            else:
                print("Your email_default setting is %s so no emails will be sent." % email_default)
        else:
            self.preferences_path = preferences_path
            self.preferences = json.load(open(preferences_path))

        if not self.enable_email:
            return

        print("Email enabled, credentials required.")
        username, password = self.get_email_credentials()
        self.email_manager = EmailManager(username, password, course, section)

    def get_dispatch_preference(self, ucid):
        """
        Get the action to take for a student email.

        :param ucid: The student's UCID
        :return: "NEVER" for never sending email, "INCORRECT" for if there was an error, or "ALWAYS"
        """
        if not self.enable_email:
            return "NEVER"

        if self.preferences is None:
            return self.email_default

        if self.course not in self.preferences:
            return self.email_default

        course_pref = self.preferences[self.course]

        if self.section not in course_pref:
            return self.email_default

        section_pref = course_pref[self.section]

        if ucid not in section_pref:
            return self.email_default

        return section_pref[ucid]

    def dispatch_email(self, submitter_ucid, printout, error=False):
        """
        Tell the EmailDispatcher to send an email if warranted to a student.

        :param submitter_ucid: The student UCID.
        :param printout: What the grade printout is for the lab.
        :param error: If the lab had an error in it.
        :return:
        """
        email_case = self.get_dispatch_preference(submitter_ucid)

        if (not error and not email_case == "ALWAYS") or email_case == "NEVER":
            return

        self.email_manager.send_email(submitter_ucid, printout)

    def shutdown(self):
        """
        Shutdown the EmailDispatcher and it's EmailManager instance.
        :return:
        """
        self.email_manager.close_smtp_connection()

    @staticmethod
    def get_email_credentials():
        """
        Prompt the grader for their credentials.
        :return:
        """
        ucid = input("Please input your UCID: ")
        password = getpass()
        return ucid, password

    def handle_lab(self, lab, broken=False):

        submitter_ucid = lab.ucid

        submitter_preference = self.get_dispatch_preference(submitter_ucid)

        if submitter_preference == "NEVER":
            return

        if submitter_preference == "INCORRECT" and not broken:
            return

        self.dispatch_email(submitter_ucid, lab.get_score_report(False), broken)
