from getpass import getpass

__author__ = 'Joshua D. Katz'

__GRADER_UCID_ACCOUNT__ = None


class UCIDAccount:
    def __init__(self):
        print("UCID functionality requested.")
        print("Please input your information or type \"cancel\"")

        username = input("Please enter your username: ")

        if username.lower() == "cancel":
            self.ucid_access = False
            return
        else:
            self.ucid_access = True

        self.ucid = username
        self.password = getpass()

    def is_login_available(self):
        return self.ucid_access

    def get_ucid_credentials(self):
        return self.ucid, self.password


def get_grader_ucid_account():
    global __GRADER_UCID_ACCOUNT__
    if __GRADER_UCID_ACCOUNT__ is None:
        __GRADER_UCID_ACCOUNT__ = UCIDAccount()
    return __GRADER_UCID_ACCOUNT__
