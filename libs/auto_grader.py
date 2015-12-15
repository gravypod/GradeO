from os.path import basename

from libs.module_loader import load_module, get_module_functions, get_variables
from lab_submissions import LabScore

"""

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


class AutoGrader:
    lab_number = None
    class_section = None
    functions = None
    multiple_choice_answers = None

    def __init__(self, lab_number, class_section, module):
        """
        Create the AutoGrader file that automates the scoring/grating process.

        :param lab_number: The lab number that we are grading.
        :param class_section: The class section that we are grading.
        :param module: The module of the AutoGrader script. Loaded from .py file.
        :return: AutoGrader object.
        """
        self.lab_number = lab_number
        self.class_section = class_section
        self.functions = get_module_functions(module)

        answers = {k.lower(): v.lower() for k, v in get_variables(module).items()}
        self.multiple_choice_answers = {int(k[8:]): v for k, v in answers.items() if k.startswith("answers")}

    def get_test_functions(self):
        """
        Get all of the AutoGrader functions that are used for testing labs.

        :return: A dictionary who's keys are the function the lab tests and who's value is the instance of the function.
        """
        return {n[0:n.index("_test")]: f for n, f in self.functions.items() if n.endswith("_test")}

    def score(self, lab):
        """
        Used for scoring labs.

        :param lab: The lab to score.
        :return: Returns a string if the lab threw an exception or a score if the lab started correctly.
        """

        if not lab.has_lab_loaded():
            return lab.module

        scorer = self.functions["scorer"]

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
    """
    Get the percentage of correct written problems and their score_set.

    The percent ranges from 0.0 (for none correct) to 1.0 (for all correct).

    :param test_cases: The test functions from the AutoGrader.
    :param lab: The lab to grade.
    :return: A tuple of the percent of correctness, and a dictionary of functions names mapping to if they are correct.
    """
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
    """
    Get the percent of correct multiple choice answers.

    :param correct_answers: The set of correct answers from the AutoGrader.
    :param lab: The lab to score multiple choice questions from.
    :return: A tuple with percent of correctness, and a dictionary with question numbers pointing to True if correct.
    """

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


def load_grader(grader_path):
    """
    Load the AutoGrader's script file.

    :param grader_path: Path to the AutoGrader script file
    :return: The AutoGrader file.
    """
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
