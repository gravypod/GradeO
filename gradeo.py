import loader
from traceback import format_exc
import argparse

__author__ = 'Joshua D. Katz'


def get_format_bar(msg, length=35, c="-"):
    part_size = int((length - len(msg)) / 2)
    pad = (c * part_size)
    return pad + msg + pad


def print_incorrect_box(intro, message, outro="grade accordingly"):
    print(get_format_bar(intro))
    print()
    print(message)
    print()
    print(get_format_bar(outro))


def get_incorrect_report(incorrect_functions, incorrect_multiple_choice):

    if not incorrect_functions and not incorrect_multiple_choice:
        raise Exception("get_incorrect_report called for perfect lab.")

    message = ""

    if incorrect_functions:
        message += "There were %d incorrect functions" % len(incorrect_functions) + "\n"
        message += "\tIncorrect functions: " + ", ".join([f.__name__ for f in incorrect_functions]) + "\n"

    if incorrect_multiple_choice:
        message += "There were %d incorrect multiple choice answers" % len(incorrect_multiple_choice) + "\n"
        message += "\tIncorrect multiple choice: " + ", ".join([str(c) for c in incorrect_multiple_choice]) + "\n"

    return message


def print_lab_score(ucid, lab_score, use_short_printout):

    incorrect_functions = lab_score.get_incorrect_functions()
    incorrect_multiple_choice = lab_score.get_incorrect_multiple_choice()

    if use_short_printout or (not incorrect_multiple_choice and not incorrect_functions):
        print("%s received a %d" % (ucid, lab_score.score))
        return

    print_incorrect_box(ucid, get_incorrect_report(incorrect_functions, incorrect_multiple_choice))


def grade(grader_file, lab_submission_path, short_print):

    print("Starting grading")

    try:
        auto_grader = loader.load_grader(grader_file)
    except:
        print("Error loading AutoGrader file.")
        print(format_exc())
        return

    print("Grader loaded from section %s and lab number %d" % (auto_grader.class_section, auto_grader.lab_number))

    print("Labs loaded from %s" % lab_submission_path)

    submitted_labs = loader.load_labs(lab_submission_path, auto_grader.lab_number)

    for lab in submitted_labs:

        if not lab.has_lab_loaded():
            print_incorrect_box(lab.ucid + " has thrown", lab.module)
            continue

        try:

            lab_score = auto_grader.score(lab)

            print_lab_score(lab.ucid, lab_score, short_print)

        except:
            print(format_exc())
            print("Failed to grade lab from %s, must be graded by hand." % lab.ucid)


def main():
    parser = argparse.ArgumentParser(description="GradeO automatic lab grader")
    parser.add_argument("--grader", action="store", type=str, help="The AutoGrader file to use", required=True)
    parser.add_argument("--labs", action="store", type=str, help="Folder with labs to grade", default="labs/")
    parser.add_argument("--short_print", action="store_true", help="Folder with labs to grade", default=False)
    options = parser.parse_args()

    grade(options.grader, options.labs, options.short_print)


if __name__ == '__main__':
    main()
