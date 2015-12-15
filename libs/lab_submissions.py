from os import listdir
from os.path import join, isfile, basename
import libs.report_card as report_card
import inspect

from libs.module_loader import get_variables, load_module

"""
Used to load labs from students.

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
        """
        Creates a Lab object.

        :param ucid: The UCID of the person who submitted this work.
        :param lab_number: The lab number of who.
        :param module: The module loaded from the submitted lab file.
        :return: Lab object.
        """
        self.ucid = ucid
        self.lab_number = lab_number
        self.module = module

    def has_lab_loaded(self):
        """
        Checks to see if the lab was able to be loaded without throwing an exception.

        :return: True if the lab is loaded successfully by load_module.
        """
        return not type(self.module) is str

    def get_multiple_choice_answers(self):
        """
        Gets the values from every variable notating a multiple choice answers in the submitted lab.

        :return: A dictionary where the key is an int of the question number, and the value is the answer.
        """

        variables = {k.lower(): v.lower() for k, v in get_variables(self.module).items()}

        variables = {int(k[10:]): v for k, v in variables.items() if k.startswith("question")}

        return variables

    def get_function(self, name):
        """
        Get a function by name from the submitted lab.

        :param name: The name of the function.
        :return: An instance of the function or None if it does not exist.
        """

        attribute = getattr(self.module, name)

        if not inspect.isfunction(attribute):
            return None

        if not inspect.getmodule(attribute) == self.module:
            return None

        return attribute


class LabScore:
    score = 0
    ucid = ""
    load_error = None
    multiple_choice_score_set = None
    written_score_set = None

    def __init__(self, ucid, score, load_error, multiple_choice_score_set, written_score_set):
        """
        Create a LabScore object that contains information on the score of the lab.

        :param score: The score for the lab
        :param multiple_choice_score_set: The scored dictionary of multiple choice questions
        :param written_score_set: The scored dictionary of written questions
        :return: LabScore object
        """
        self.score = score
        self.ucid = ucid
        self.load_error = load_error
        self.multiple_choice_score_set = multiple_choice_score_set
        self.written_score_set = written_score_set

    def get_incorrect_functions(self):
        """
        Get all the functions that were graded as incorrect.

        :return: A list of the names of functions that were graded as incorrect.
        """
        if not self.written_score_set:
            return []
        return [fun for fun in self.written_score_set if not self.written_score_set[fun]]

    def get_incorrect_multiple_choice(self):
        """
        Get all the multiple choice answers that were incorrect.

        :return: A list of the number for every question that was wrong.
        """
        if not self.multiple_choice_score_set:
            return []
        return [fun for fun in self.multiple_choice_score_set if not self.multiple_choice_score_set[fun]]

    def has_load_error(self):
        return self.load_error is not None or self.score is None

    def is_lab_correct(self):
        if self.has_load_error():
            return False

        return len(self.get_incorrect_functions() + self.get_incorrect_multiple_choice()) == 0

    def get_score_report(self,  short_hand):
        functions_incorrect = self.get_incorrect_functions()
        mc_incorrect = self.get_incorrect_multiple_choice()

        if self.has_load_error():
            return report_card.get_error_report(self.ucid, self.load_error)

        if not short_hand:
            return report_card.get_incorrect_report(self.ucid, self.score, functions_incorrect, mc_incorrect)

        return "%s received a %d" % (self.ucid, self.score)


def load_labs(lab_folder, lab_number):
    """
    Load all of the submitted lab files from within a directory.

    :param lab_folder: Folder containing all submitted labs.
    :param lab_number: The lab number we are looking to grade.
    :return: A list of Lab objects representing loaded labs.
    """
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


def get_lab_from_filename(code_path):
    """
    Get the lab number from a lab submission file name.

    :param code_path: The path to, or file name of, a submitted lab.
    :return: None if parsing was uncompleted or a int parsed from the file name.
    """
    file_name = basename(code_path)

    lab_number = file_name[2:5]

    if not lab_number.isdigit():
        return None

    return int(lab_number)


def get_ucid_from_filename(code_path):
    """
    Get the UCID from a submitted lab file.

    :param code_path: The path to, or file name of, a submitted lab.
    :return: The UCID of the submitter.
    """
    file_name = basename(code_path)

    ucid_start = file_name.index("_") + 1
    ucid_end = file_name.index(".")

    return file_name[ucid_start:ucid_end]
