import os
from os import listdir
from os.path import isfile, basename, dirname, relpath, join
from traceback import format_exc
import inspect
import importlib

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

    def has_lab_loaded(self):
        """Return true if the lab is loadable by python (no errors)"""
        return not type(self.module) is str

    def get_multiple_choice_answers(self):
        """Get all the multiple choice answers this lab."""

        variables = {k.lower(): v.lower() for k, v in get_variables(self.module).items()}

        variables = {int(k[10:]): v for k, v in variables.items() if k.startswith("question")}

        return variables

    def get_function(self, name):
        """Get a function from this lab. The name is the name of the function."""

        attribute = getattr(self.module, name)

        if not inspect.isfunction(attribute):
            return None

        if not inspect.getmodule(attribute) == self.module:
            return None

        return attribute


class LabScore:

    score = 0
    multiple_choice_score_set = None
    written_score_set = None

    def __init__(self, score, multiple_choice_score_set, written_score_set):
        self.score = score
        self.multiple_choice_score_set = multiple_choice_score_set
        self.written_score_set = written_score_set

    def get_incorrect_functions(self):
        return [fun for fun in self.written_score_set if not self.written_score_set[fun]]

    def get_incorrect_multiple_choice(self):
        return [fun for fun in self.multiple_choice_score_set if not self.multiple_choice_score_set[fun]]


class AutoGrader:
    lab_number = None
    class_section = None
    functions = None
    multiple_choice_answers = None

    def __init__(self, lab_number, class_section, module):
        self.lab_number = lab_number
        self.class_section = class_section
        self.functions = get_module_functions(module)

        answers = {k.lower(): v.lower() for k, v in get_variables(module).items()}
        self.multiple_choice_answers = {int(k[8:]): v for k, v in answers.items() if k.startswith("answers")}

    def get_test_functions(self):
        """Get all the AutoGrader functions dedicated to testing student written lab functions"""
        return {n[0:n.index("_test")]: f for n, f in self.functions.items() if n.endswith("_test")}

    def score(self, lab):
        """Returns score for the lab passed. Returns -1 if the lab could not load."""

        scorer = self.functions["scorer"]

        if not lab.has_lab_loaded():
            return -1

        multiple_choice_response = (0, None)
        written_section_response = (0, None)

        function_tests = self.get_test_functions()

        if self.multiple_choice_answers:
            multiple_choice_response = get_percent_multiple_correct(self.multiple_choice_answers, lab)

        if function_tests:
            written_section_response = get_percent_written_correct(function_tests, lab)

        score = scorer(multiple_choice_response[0], written_section_response[0])

        return LabScore(score, multiple_choice_response[1], written_section_response[1])


def get_percent_written_correct(test_cases, lab):
    """Returns the percentage from 0.0 to 1.0 of correct written questions"""

    correct = 0
    total = len(test_cases)
    score_set = {}

    for number, test in test_cases.items():

        written_function = lab.get_function(number)

        score_set[number] = False

        if written_function is None:
            continue

        if not test(written_function):
            continue

        score_set[number] = True
        correct += 1

    return correct / total, score_set


def get_percent_multiple_correct(correct_answers, lab):
    """Returns the percentage from 0.0 to 1.0 of correct multiple choice questions"""

    lab_answers = lab.get_multiple_choice_answers()
    correct = 0
    total = len(correct_answers)
    score_set = {}

    for number, answer in correct_answers.items():
        score_set[number] = False
        if number not in lab_answers:
            continue
        if not answer == lab_answers[number]:
            continue
        score_set[number] = True
        correct += 1

    return correct / total, score_set


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
    ucid_end = file_name.index(".")

    return file_name[ucid_start:ucid_end]


def load_module(code_path):
    """Load a module from it's path. The code_path is a path to the file."""
    if not isfile(code_path):
        return None

    try:

        # Magic module loading
        code_dir = dirname(relpath(code_path))
        code_file = basename(code_path)
        module_path = code_dir.replace(os.sep, ".")
        module_name = code_file[0:code_file.index(".")]

        # code_package = relpath(dirname(code_path)).replace(os.sep, ".")

        # if code_dir == ".":
        # print(code_dir)
        # print(code_file)
        # print(module_path)
        # print(module_name)
        # print("%s.%s" % (module_path, module_name))
        return importlib.import_module("%s.%s" % (module_path, module_name))  # , fromlist=["*"])
        # else:
        #    module = __import__(module_name, fromlist=["*"])
        # return importlib.import_module(code_package + "." + module_name)

    # Must handle ANY exception.
    # This will come from the module we are loading.
    # Any exception thrown is from the student's code.
    except:

        # print("%s failed to load" % code_path)
        # traceback.format_exec() returns a string.
        # The string is the text that the exception would have been thrown.
        return format_exc()


def load_labs(lab_folder, lab_number):
    labs = []

    for lab_file_name in listdir(lab_folder):

        lab_path = join(lab_folder, lab_file_name)

        if not isfile(lab_path):
            continue

        if not lab_path.endswith(".py"):
            print("Bad file in labs directory %s" % lab_path)
            continue

        submission_ucid = get_ucid_from_filename(lab_file_name)
        submission_lab_number = get_lab_from_filename(lab_file_name)

        if not submission_lab_number == lab_number:
            # TODO: Some form of logging to tell the TA that there is a problem
            print("Incorrect lab in lab folder from %s" % submission_ucid)
            continue

        module = load_module(lab_path)

        labs.append(Lab(submission_ucid, submission_lab_number, module))

    return labs


def load_grader(grader_path):
    """Load AutoGrader module from grader_path"""

    grader_file = basename(grader_path)

    number = grader_file[2:5]

    if not number.isdigit():
        print("AutoGrader number cannot be parsed. Number is %s" % number)
        raise Exception("AutoGrader name is formatted incorrectly %s " % grader_path)

    number = int(number)

    section = grader_file[-6:-3]
    module = load_module(grader_path)

    if type(module) is str:
        print(module)
        raise Exception("Error loading AutoGrader module")

    return AutoGrader(number, section, module)
