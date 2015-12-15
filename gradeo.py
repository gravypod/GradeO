from traceback import format_exc
import argparse

from libs.auto_grader import load_grader
from libs.lab_submissions import load_labs
from libs.report_card import print_incorrect_box, print_lab_score
from libs.email_dispatcher import EmailDispatcher
from libs import file_utilities

__author__ = 'Joshua D. Katz'


def grade_labs(auto_grader, lab_submission_path):
    """
    This function loads the grader_file, runs it's score method against anything in the folder for lab_submission_path.
    This is will return data but print out an absolute minimum amount of information.

    :param grader_file: The path to the AutoGrader file
    :param lab_submission_path: The path to the folder containing lab submissions
    :return: A dictionary who's keys are UCID (Strings) and values are ints if can be graded, or strings for errors.
    """

    print("Labs loaded from %s" % lab_submission_path)

    submitted_labs = load_labs(lab_submission_path, auto_grader.lab_number)

    scored_labs = {}

    for lab in submitted_labs:
        ucid = lab.ucid
        try:
            score = auto_grader.score(lab)
            scored_labs[lab.ucid] = score
        except:
            print_incorrect_box("Can't grade for %s" % ucid, "Exception thrown:\n" + format_exc(), "Grade by hand.")

    return scored_labs


def grade(auto_grader, lab_submission_path, short_print, emailer):
    """
    Call grade_labs and print out grade report
    :param auto_grader: The AutoGrader to use for scoring.
    :param lab_submission_path: The lab submission folder path.
    :param short_print: If set to true, printing will always attempt to be in short form.
    :return:
    """
    graded_labs = grade_labs(auto_grader, lab_submission_path)

    for ucid, score in graded_labs.items():

        # This happens when the load_module function in module_loader.py returned a string.

        print(score.get_score_report(short_print))

        emailer.dispatch_email(score.ucid, score.get_score_report(False), score.is_lab_correct())


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

    email_option_group = parser.add_argument_group("Email Dispatcher", "Send's email's to students")

    email_option_group.add_argument("--enable_email", action="store_true",
                                    help="Tells GradeO to email students their grades",
                                    default=False)

    email_option_group.add_argument("--email_pref", action="store",
                                    help="Tells GradeO what file to pull email dispatch preferences from.",
                                    default="email_dispatch.json",
                                    required=False)

    email_option_group.add_argument("--email_default", action="store",
                                    help="Sets the default send option.",
                                    default="NEVER")

    parser.add_argument_group(email_option_group)

    # Parse arguments from command line arguments
    options = parser.parse_args()

    # Pass to grade functionality
    try:
        auto_grader = load_grader(options.grader)
        course = auto_grader.course
        section = auto_grader.section
        print("Grader loaded: Course %s-%s and lab number %0.3d" % (course, section, auto_grader.lab_number))
    except:
        print("Error loading AutoGrader file.")
        print(format_exc())
        return
    email_sender = EmailDispatcher(options.enable_email, options.email_default, options.email_pref, course, section)
    grade(auto_grader, options.labs, options.short_print, email_sender)


if __name__ == '__main__':
    main()
