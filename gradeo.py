from traceback import format_exc
import argparse

from os import sep
from libs.auto_grader import load_grader
from libs.csv_manager import CSVManager
from libs.lab_submissions import load_labs
from libs.email_manager import EmailDispatcher
from libs.finished_manager import FinishedLabManager
from libs.output_manager import ConsoleOutputManager
from libs.move_finished_manager import MoveFinishedLabHandler
from libs.cheating_manager import CheatingManager
from libs import argparse_validation

__author__ = 'Joshua D. Katz'


def main():
    """
    Run when gradeo is run as the main file.
    This only happens when it is not imported as a module
    :return: Nothing
    """
    parser = argparse.ArgumentParser(description="GradeO automatic lab grader")

    # AutoGrader file location argument
    parser.add_argument("--grader", action="store",
                        type=argparse_validation.is_file,
                        help="The AutoGrader file to use",
                        required=True)

    # Labs folder location argument
    parser.add_argument("--labs", action="store",
                        type=argparse_validation.is_folder,
                        help="Folder with labs to grade",
                        default="labs" + sep)

    # Move lab after grading into a file
    parser.add_argument("--move_finished", action="store",
                        type=str,
                        help="Move graded labs into this directory after processing if the directory exists.",
                        default="graded" + sep)

    # Short Print option flag
    parser.add_argument("--short_print", action="store_true",
                        help="Prefer short hand printing in console output",
                        default=False)

    parser.add_argument("--csv", action="store",
                        help="Set a file to store the grades in CSV format to.",
                        default="")

    parser.add_argument("--find_similar", "--find_pumpkin_eaters", "--find_pants_on_fire", action="store_true",
                        help="Enable a SUPER ALPHA similarity finder. Will take forever to run.",
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
                                    type=argparse_validation.is_acceptable_email_default,
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

    email_options = [options.enable_email, options.email_default, options.email_pref]
    email_manager = EmailDispatcher(*email_options, course=course, section=section)

    output_manager = ConsoleOutputManager(options.short_print)

    move_finished_handler = MoveFinishedLabHandler(options.move_finished)

    csv_manager = CSVManager(options.csv, auto_grader.lab_number)

    cheating_manager = CheatingManager(options.find_similar)

    finished_lab_manager = FinishedLabManager([
        output_manager,
        move_finished_handler,
        email_manager,
        csv_manager,
        cheating_manager
    ])

    email_manager.shutdown()

    finished_lab_manager.handle_graded_lab(load_labs(auto_grader, options.labs))


if __name__ == '__main__':
    main()
