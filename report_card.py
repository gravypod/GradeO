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
