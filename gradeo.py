from traceback import format_exc
import argparse

from libs.auto_grader import load_grader
from libs.lab_submissions import load_labs
from libs.report_card import print_incorrect_box, print_lab_score
from libs import file_utilities

__author__ = 'Joshua D. Katz'


def grade_labs(grader_file, lab_submission_path):
    """
    This function loads the grader_file, runs it's score method against anything in the folder for lab_submission_path.
    This is will return data but print out an absolute minimum amount of information.

    :param grader_file: The path to the AutoGrader file
    :param lab_submission_path: The path to the folder containing lab submissions
    :return: A dictionary who's keys are UCID (Strings) and values are ints if can be graded, or strings for errors.
    """
    try:
        auto_grader = load_grader(grader_file)
        print("Grader loaded: section %s and lab number %0.3d" % (auto_grader.class_section, auto_grader.lab_number))
    except:
        print("Error loading AutoGrader file.")
        print(format_exc())
        return

    print("Labs loaded from %s" % lab_submission_path)

    submitted_labs = load_labs(lab_submission_path, auto_grader.lab_number)

    scored_labs = {}

    for lab in submitted_labs:
        ucid = lab.ucid
        score = auto_grader.score(lab)
        try:
            scored_labs[lab.ucid] = score
        except:
            print_incorrect_box("Can't grade for %s" % ucid, "Exception thrown:\n" + format_exc(), "Grade by hand.")

    return scored_labs


def grade(grader_file, lab_submission_path, short_print):
    """
    Call grade_labs and print out grade report
    :param grader_file: The AutoGrader file path
    :param lab_submission_path: The lab submission folder path
    :param short_print: If set to true, printing will always atempt to be in short form
    :return:
    """
    graded_labs = grade_labs(grader_file, lab_submission_path)

    for ucid, score in graded_labs.items():

        # This happens when the load_module function in module_loader.py returned a string.
        if type(score) is str:
            print_incorrect_box(ucid + " has thrown", score)
            continue

        print_lab_score(ucid, score, short_print)


def main():
    """
    Run when gradeo is run as the main file.
    This only happens when it is not imported as a module
    :return: Nothing
    """
    parser = argparse.ArgumentParser(description="GradeO automatic lab grader")

    # AutoGrader file location argument
    parser.add_argument("--grader", action="store",
                        type=file_utilities.is_file,
                        help="The AutoGrader file to use",
                        required=True)

    # Labs folder location argument
    parser.add_argument("--labs", action="store",
                        type=file_utilities.is_folder,
                        help="Folder with labs to grade",
                        default="labs/")

    # Short Print option flag
    parser.add_argument("--short_print", action="store_true",
                        help="Folder with labs to grade",
                        default=False)

    # Parse arguments from command line arguments
    options = parser.parse_args()

    # Pass to grade functionality
    grade(options.grader, options.labs, options.short_print)


if __name__ == '__main__':
    main()
