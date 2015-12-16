from os.path import basename

from libs.module_loader import load_module, get_module_functions, get_variables

"""

Grades are calculated from grader files.
A grader is specified as follows:

    The current agreed upon format for grader files is as follows:

        hw001_cs100_h01.py

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


class AutoGrader:
    lab_number = None
    course = None
    section = None
    functions = None
    multiple_choice_answers = None

    def __init__(self, lab_number, course, section, module):
        """
        Create the AutoGrader file that automates the scoring/grating process.

        :param lab_number: The lab number that we are grading.
        :param course: The class section that we are grading.
        :param module: The module of the AutoGrader script. Loaded from .py file.
        :return: AutoGrader object.
        """
        self.lab_number = lab_number
        self.course = course
        self.section = section
        self.functions = get_module_functions(module)

        answers = {k.lower(): v.lower() for k, v in get_variables(module).items()}
        self.multiple_choice_answers = {int(k[8:]): v for k, v in answers.items() if k.startswith("answers")}

    def get_test_functions(self):
        """
        Get all of the AutoGrader functions that are used for testing labs.

        :return: A dictionary who's keys are the function the lab tests and who's value is the instance of the function.
        """
        return {n[0:n.index("_test")]: f for n, f in self.functions.items() if n.endswith("_test")}

    def score(self, lab_functions_defined, lab_multiple_choice_answers):

        if not lab_functions_defined and not lab_multiple_choice_answers:
            return None, None, None

        scorer = self.functions["scorer"]

        multiple_choice_response = (0, None)
        written_section_response = (0, None)

        function_tests = self.get_test_functions()

        if self.multiple_choice_answers:
            correct_answers = self.multiple_choice_answers
            multiple_choice_response = get_percent_multiple_correct(correct_answers, lab_multiple_choice_answers)

        if function_tests:
            written_section_response = get_percent_written_correct(function_tests, lab_functions_defined)

        score = scorer(multiple_choice_response[0], written_section_response[0])

        return score, multiple_choice_response[1], written_section_response[1]


def get_percent_written_correct(test_cases, lab_functions_defined):
    correct = 0
    total = len(test_cases)
    score_set = {}

    for name, test in test_cases.items():

        score_set[name] = name in lab_functions_defined and test(lab_functions_defined[name])

        if score_set[name]:
            correct += 1

    return correct / total, score_set


def get_percent_multiple_correct(correct_answers, lab_multiple_choice_answers):
    correct = 0
    total = len(correct_answers)
    score_set = {}

    for number, answer in correct_answers.items():
        score_set[number] = number in lab_multiple_choice_answers and answer == lab_multiple_choice_answers[number]
        if score_set[number]:
            correct += 1

    return correct / total, score_set


def load_grader(grader_path):
    """
    Load the AutoGrader's script file.

    :param grader_path: Path to the AutoGrader script file
    :return: The AutoGrader file.
    """
    grader_file = basename(grader_path)

    first_underscore = grader_file.index("_")
    last_underscore = grader_file.rindex("_")
    period = grader_file.rindex(".")

    number = grader_file[2:first_underscore]

    if not number.isdigit():
        print("AutoGrader number cannot be parsed. Number is %s" % number)
        raise Exception("AutoGrader name is formatted incorrectly %s " % grader_path)

    number = int(number)

    course = grader_file[first_underscore + 1:last_underscore]

    section = grader_file[last_underscore + 1:period]
    module = load_module(grader_path)

    if type(module) is str:
        print(module)
        raise Exception("Error loading AutoGrader module")

    return AutoGrader(number, course, section, module)
