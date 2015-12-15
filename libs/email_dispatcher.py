from libs.email_manager import send_email, close_smtp_connection
from getpass import getpass
from os.path import exists, isfile
import json

__author__ = "Joshua D. Katz"


class EmailDispatcher:
    def __init__(self, enable_email, email_default, preferences_path, course, section):

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
        username, password = get_email_credentials()
        self.username = username
        self.password = password

    def get_dispatch_preference(self, ucid):

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

        email_case = self.get_dispatch_preference(submitter_ucid)

        if (not error and not email_case == "ALWAYS") or email_case == "NEVER":
            return

        send_email(self.username, self.password, self.course, self.section, submitter_ucid, printout)

    @staticmethod
    def shutdown():
        close_smtp_connection()


def get_email_credentials():
    ucid = input("Please input your UCID: ")
    password = getpass()
    return ucid, password
