from os import listdir
from os.path import join, isfile, basename
from libs.report_card import get_incorrect_report, get_error_report
from libs.module_loader import get_variables, load_module, get_module_functions
from traceback import format_exc

"""
Used to load labs from students.

    The current agreed upon format for files is as follows:

        hw001_jk369.py


    All multiple choice answers are formatted as follows:

        QUESTION_1 = "A"

"""

__author__ = 'Joshua D. Katz'


class GraderNotAcceptable(Exception):
    pass


class GradeOFailed(Exception):
    def __init__(self, gradeo_error):
        self.gradeo_error = gradeo_error


class Lab:
    def __init__(self, auto_grader, lab_path):
        self.lab_number = self.get_lab_from_filename(lab_path)
        self.ucid = self.get_ucid_from_filename(lab_path)
        self.lab_path = lab_path
        self.module = load_module(lab_path)
        self.multiple_choice_answers = None
        self.score = None
        self.functions_incorrect = None
        self.multiple_choice_incorrect = None

        if self.lab_number is not auto_grader.lab_number:
            raise GraderNotAcceptable("Attempted to use incorrect AutoGrader for grading.")

        if type(self.module) is str:
            print("Error grading lab.")
            print(self.module)
            return

        functions_defined = get_module_functions(self.module)
        multiple_choice_responses = self.find_multiple_choice_answers(get_variables(self.module))

        try:
            score, mc_report, function_report = auto_grader.score(functions_defined, multiple_choice_responses)
        except:
            raise GradeOFailed("GradeO Failed to load lab from %s.\n%s\n" % (self.ucid, format_exc()))

        self.multiple_choice_answers = multiple_choice_responses
        self.score = score
        self.functions_incorrect = {f: correct for f, correct in function_report.items() if not correct}
        self.multiple_choice_incorrect = {number: correct for number, correct in mc_report.items() if not correct}

    def has_graded_successfully(self):
        return type(self.module) is not str

    @staticmethod
    def find_multiple_choice_answers(variables):
        """
        Gets the values from every variable notating a multiple choice answers in the submitted lab.

        :param variables: The variables to pull from
        :return:
        """

        return {int(k[10:]): v.lower() for k, v in variables.items() if k.lower().startswith("question")}

    def has_load_error(self):
        return self.score is None and type(self.module) is str

    def is_lab_correct(self):
        if self.has_load_error():
            return False

        if self.functions_incorrect is None or self.multiple_choice_incorrect is None:
            return False

        return len(self.functions_incorrect) + len(self.multiple_choice_incorrect) == 0

    def get_score_report(self, short_hand):

        if self.has_load_error():
            return get_error_report(self.ucid, self.module)

        if not short_hand and not self.is_lab_correct():
            return get_incorrect_report(self.ucid, self.score, self.functions_incorrect, self.multiple_choice_incorrect)

        return "%s received a %d" % (self.ucid, self.score)

    @staticmethod
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

    @staticmethod
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


def load_labs(auto_grader, lab_folder):
    labs = []

    for lab_file_name in listdir(lab_folder):

        lab_path = join(lab_folder, lab_file_name)

        if not isfile(lab_path):
            continue

        if not lab_path.endswith(".py"):
            print("Bad file in labs directory %s" % lab_path)
            continue

        try:
            lab = Lab(auto_grader, lab_path)
        except GraderNotAcceptable:
            print("Submission for wrong lab number in folder: %s" % lab_folder)
            continue
        except GradeOFailed as e:
            print(e.gradeo_error)
            continue

        labs.append(lab)

    return labs
