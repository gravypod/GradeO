import smtplib
from os.path import basename
from traceback import print_exc
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

__author__ = 'Joshua D. Katz'
__SMTP_CONNECTION__ = None


def get_email(ucid):
    return "%s@njit.edu" % ucid


def get_smtp_connection(grader_ucid, password):
    global __SMTP_CONNECTION__
    if __SMTP_CONNECTION__ is None:
        __SMTP_CONNECTION__ = smtplib.SMTP("smtp.gmail.com:587")
        __SMTP_CONNECTION__.starttls()
        __SMTP_CONNECTION__.login(get_email(grader_ucid), password)
    return __SMTP_CONNECTION__


def close_smtp_connection():
    global __SMTP_CONNECTION__
    tmp = __SMTP_CONNECTION__
    __SMTP_CONNECTION__ = None
    if tmp is not None:
        tmp.quit()


def is_smtp_connection_open():
    global __SMTP_CONNECTION__
    return __SMTP_CONNECTION__ is not None


def get_mime_multipart_email(sender, receiver, message, subject, attachments):
    email = MIMEMultipart()

    email["From"] = sender
    email["To"] = receiver
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


def send_email(grader_ucid, password, course, section, submitter_ucid, message, subject=None, attachments=None):
    try:
        connection = get_smtp_connection(grader_ucid, password)

        if subject is None:
            subject = "%s-%s email from %s" % (course, section, grader_ucid)

        grader_address = get_email(grader_ucid)
        submitter_address = get_email(submitter_ucid)
        email = get_mime_multipart_email(grader_address, submitter_address, message, subject, attachments)

        connection.sendmail(grader_address, submitter_address, email.as_string())
    except smtplib.SMTPAuthenticationError:
        print_exc()
        close_smtp_connection()
