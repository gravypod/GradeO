import argparse
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
    raise argparse.ArgumentTypeError("%s is not an existing file" % path)


def is_folder(path):
    """
    Checks to see if a path represents an existing folder
    :param path: The path to check
    :return:
    """
    if exists(path) and isdir(path):
        return path
    raise argparse.ArgumentTypeError("%s is not an existing folder" % path)
