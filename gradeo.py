import loader
from traceback import format_exc
import argparse

__author__ = 'Joshua D. Katz'


def grade(grader_file, lab_submission_path):

    try:
        auto_grader = loader.load_grader(grader_file)
    except:
        print("Error loading AutoGrader file.")
        print(format_exc())
        return

    submitted_labs = loader.load_labs(lab_submission_path, auto_grader.lab_number)

    for lab in submitted_labs:

        if not lab.has_lab_loaded():

            print("%s has not turned in a working lab.")
            print("It threw an exception.")
            print("___________________________________")
            print()
            print(lab.module)
            print()
            print("___________________________________")

            continue

        try:
            lab_score = auto_grader.score(lab)
            print("%s received a %d" % (lab.ucid, lab_score))
        except:
            print("Failed to grade lab from %s, must be graded by hand." % lab.ucid)


def main():
    parser = argparse.ArgumentParser(description="GradeO automatic lab grader")
    parser.add_argument("--labs", type=str, default="labs/")
    parser.add_argument("--grader", type=argparse.FileType("r"))
    options = parser.parse_args()

    grade(options.grader, options.labs)


if __name__ == '__main__':
    main()
