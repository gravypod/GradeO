import argparse
from os.path import exists, isdir, isfile

__author__ = 'Joshua D. Katz'


def is_file(path):
    if exists(path) and isfile(path):
        return path
    raise argparse.ArgumentTypeError("%s is not an existing file" % path)


def is_folder(path):
    if exists(path) and isdir(path):
        return path
    raise argparse.ArgumentTypeError("%s is not an existing folder" % path)
