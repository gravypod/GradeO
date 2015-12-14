from os.path import isfile, basename, dirname, relpath
from traceback import format_exc
"""
Used to labs from students.

The current agreed upon format for files is as follows:

hw001_jk369.py
"""

__author__ = 'Joshua D. Katz'


def get_ucid_from_filename(code_path):
    """Get UCID from file path. The code_dir is the path to the lab you want to pull the UCID from."""
    file_name = basename(code_path)
    ucid_start = file_name.index("_") + 1
    ucid_end = file_name.index("_")
    return file_name[ucid_start:ucid_end]


def load_module(code_path):
    """Load a module from it's path. The code_path is a path to the file."""
    if not isfile(code_path):
        return None

    try:

        # Magic module loading
        code_dir = relpath(dirname(code_path))
        code_file = basename(code_path)

        module_name = code_file[0:code_file.index(".")]

        module = __import__("%s.%s" % (code_dir, module_name), fromlist=["*"])

        return module

    # Must handle ANY exception.
    # This will come from the module we are loading.
    # Any exception thrown is from the student's code.
    except BaseException:

        print("%s failed to load" % code_path)
        # traceback.format_exec() returns a string.
        # The string is the text that the exception would have been thrown.
        return format_exc()
