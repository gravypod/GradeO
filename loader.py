from os.path import isfile, basename, dirname, relpath
from traceback import format_exc
import inspect

"""
Used to labs from students.

    The current agreed upon format for files is as follows:

        hw001_jk369.py


    All multiple choice answers are formatted as follows:

        QUESTION_1 = "A"

Grades are calculated from grader files.
A grader is specified as follows:

    The current agreed upon format for grader files is as follows:

        hw001_h01.py

    All multiple choice answers are formatted as follows:

        ANSWER_1 = "B"

    Any test suits written for student lab files is as follows:

        def student_given_function_name_test(student_implementation)

        This will grade any student function named:
            "student_given_function_name"

        The students must use function names given in labs. For this, we must use PEP compliant naming in labs.

        The test function will be able to run the student implementation as follows:
            student_implementation(parameters)

        The graders must also implement at scorer method:
            This method is used to calculate the final score for labs.
            The method must accept two variables:
                The first is the percent, 0.0 to 1.0, of multiple choice answers correct.
                The second is the percent, 0.0 to 1.0, of written answers correct.

                This method must return the score for the lab submission.
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

    def get_multiple_choice_answers(self):
        """Get all the multiple choice answers this lab."""

        variables = {k.lower(): v.lower() for k, v in get_variables(self.module).items()}

        return {int(k[9:]): v for k, v in variables.items() if k.startswith("question")}

    def get_function(self, name):
        """Get a function from this lab. The name is the name of the function."""

        attribute = getattr(self.module, name)

        if not inspect.isfunction(attribute):
            return None

        if not inspect.getmodule(attribute) == self.module:
            return None

        return attribute


class AutoGrader:
    lab_number = None
    functions = None
    multiple_choice_answers = None

    def __init__(self, lab_number, module):
        self.lab_number = lab_number
        self.functions = get_module_functions(module)

        answers = {k.lower(): v.lower() for k, v in get_variables(module).items()}
        self.multiple_choice_answers = {int(k[8:]): v for k, v in answers.items() if k.startswith("answers")}

    def get_test_functions(self):
        return {n[0:n.index("_test")]: f for n, f in self.functions.items() if n.endswith("_test")}

    def score(self, lab):

        multiple_choice_correct = 0
        written_correct = 0

        function_tests = self.functions

        if self.multiple_choice_answers:
            multiple_choice_correct = get_percent_multiple_correct(self.multiple_choice_answers, lab)

        if function_tests:
            written_correct = get_percent_written_correct(function_tests, lab)

        scorer = self.functions["scorer"]

        return scorer(multiple_choice_correct, written_correct)


def get_percent_written_correct(test_cases, lab):

    correct = 0
    total = len(test_cases)

    for number, test in test_cases:

        written_function = lab.get_function(number)

        if written_function is None:
            continue

        if not test(written_function):
            continue

        correct += 1

    return correct / total


def get_percent_multiple_correct(correct_answers, lab):

    lab_answers = lab.get_multiple_choice_answers()
    correct = 0
    total = len(correct_answers)

    for number, answer in correct_answers:

        if number not in lab_answers:
            continue
        if not answer == lab_answers[number]:
            continue
        correct += 1

    return correct / total


def get_variables(module):
    """Get all of the variables declared in module."""

    def is_var(item):
        return not inspect.isfunction(item) and inspect.getmodule(item) is None

    module_attributes = {k: getattr(module, k) for k in module.__dict__.keys()}

    return {k: v for k, v in module_attributes.items() if is_var(v) and not k.startswith("__")}


def is_function(mod, func):
    return inspect.isfunction(func) and inspect.getmodule(func) == mod


def get_module_functions(mod):
    return {func.__name__: func for func in mod.__dict__.values() if is_function(mod, func)}


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
