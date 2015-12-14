from os.path import isfile, basename, dirname, relpath
from traceback import format_exc
import inspect
"""
Used to labs from students.

The current agreed upon format for files is as follows:

hw001_jk369.py


All multiple choice answers are formatted as follows:

QUESTION_1 = "A"

"""

__author__ = 'Joshua D. Katz'


class Lab:

    ucid = None
    lab_number = None
    module = None

    def __init__(self, ucid, lab_number, module):
        self.ucid = ucid
        self.lab_number = lab_number
        self.module = module

    def get_variables(self):

        def is_var(item):
            return not inspect.isfunction(item) and inspect.getmodule(item) is None

        module_attributes = {k: getattr(self.module, k) for k in self.module.__dict__.keys()}

        return {k: v for k, v in module_attributes.items() if is_var(v) and not k.startswith("__")}

    def get_multiple_choice_answers(self):

        variables = {k.lower(): v.lower() for k, v in self.get_variables().items()}

        return {int(k[9:]): v for k, v in variables.items() if k.startswith("question")}

    def get_function(self, name):

        attribute = getattr(self.module, name)

        if not inspect.isfunction(attribute):
            return None

        if not inspect.getmodule(attribute) == self.module:
            return None

        return attribute


def get_lab_from_filename(code_path):
    """Get lab numbers from the lab number files. The code_path is the path to the lab."""
    file_name = basename(code_path)

    lab_number = file_name[2:5]

    if not lab_number.isdigit():
        return None

    return int(lab_number)


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
