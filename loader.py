from os.path import isfile, basename, dirname, relpath
from traceback import format_exc
"""
Used to load files from
"""

__author__ = 'Joshua D. Katz'


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
