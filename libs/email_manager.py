import smtplib
from os.path import basename
from traceback import print_exc
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

__author__ = 'Joshua D. Katz'


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
