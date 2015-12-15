import loader
from traceback import format_exc
from report_card import print_incorrect_box, print_lab_score
import argparse

__author__ = 'Joshua D. Katz'


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
