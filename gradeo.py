import loader
from traceback import format_exc
from report_card import print_incorrect_box, print_lab_score
import argparse

__author__ = 'Joshua D. Katz'


def grade_labs(grader_file, lab_submission_path):
    try:
        auto_grader = loader.load_grader(grader_file)
        print("Grader loaded from section %s and lab number %0.3d" % (auto_grader.class_section, auto_grader.lab_number))
    except:
        print("Error loading AutoGrader file.")
        print(format_exc())
        return

    print("Labs loaded from %s" % lab_submission_path)

    submitted_labs = loader.load_labs(lab_submission_path, auto_grader.lab_number)

    return {lab.ucid: auto_grader.score(lab) for lab in submitted_labs}


def grade(grader_file, lab_submission_path, short_print):
    graded_labs = grade_labs(grader_file, lab_submission_path)

    for ucid, score in graded_labs.items():

        # This happens when the load_module function in loader.py returned a string.
        if type(score) is str:
            print_incorrect_box(ucid + " has thrown", score)
            continue

        try:

            print_lab_score(ucid, score, short_print)

        except:
            print(format_exc())
            print("Failed to grade lab from %s, must be graded by hand." % ucid)


def main():
    parser = argparse.ArgumentParser(description="GradeO automatic lab grader")
    parser.add_argument("--grader", action="store", type=str, help="The AutoGrader file to use", required=True)
    parser.add_argument("--labs", action="store", type=str, help="Folder with labs to grade", default="labs/")
    parser.add_argument("--short_print", action="store_true", help="Folder with labs to grade", default=False)
    options = parser.parse_args()

    grade(options.grader, options.labs, options.short_print)


if __name__ == '__main__':
    main()
