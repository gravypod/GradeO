from libs.email_manager import EmailManager
from getpass import getpass
from os.path import exists, isfile
import json

__author__ = "Joshua D. Katz"


class EmailDispatcher:
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
