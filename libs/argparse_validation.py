from argparse import ArgumentTypeError
from os.path import exists, isdir, isfile

__author__ = 'Joshua D. Katz'


def is_file(path):
    """
    Checks to see if a path represents an existing file
    :param path: The path to check
    :return:
    """
    if exists(path) and isfile(path):
        return path
    raise ArgumentTypeError("%s is not an existing file" % path)


def is_folder(path):
    """
    Checks to see if a path represents an existing folder
    :param path: The path to check
    :return:
    """
    if exists(path) and isdir(path):
        return path
    raise ArgumentTypeError("%s is not an existing folder" % path)


def is_acceptable_email_default(default):
    """
    Checks to see if a path represents an existing folder
    :param default: Validate the email_default setting.
    :return:
    """
    acceptable_email_default = ["NEVER", "ALWAYS", "INCORRECT"]

    if default not in acceptable_email_default:
        acceptable_string = ", ".join(acceptable_email_default)
        raise ArgumentTypeError("%s is not acceptable email default setting. Must be %s" % (default, acceptable_string))

    return default
