__author__ = 'Joshua D. Katz'


def get_format_bar(msg, length=35, c="-"):
    """
    Get a string, padded with characters on either side.
    Used to format things for printing.

    :param msg: The message to center inside the bar.
    :param length: The length of finished bar. Defaults to 35 characters.
    :param c: The character to pad both sides with.
    :return: The padded bar with a message in the middle.
    """
    part_size = int((length - len(msg)) / 2)
    pad = (c * part_size)
    return pad + msg + pad


def print_incorrect_box(intro, message, outro="grade accordingly"):
    """
    Print a report of an incorrect lab.

    :param intro: The message to put at the top of the box.
    :param message: The message to put inside the box.
    :param outro: The message to put on the bottom of the box.
    :return: None
    """
    print(get_format_bar(intro))
    print()
    print(message)
    print()
    print(get_format_bar(outro))


def get_incorrect_report(incorrect_functions, incorrect_multiple_choice):
    """
    Get the message contents to print out for an incorrect lab.

    :param incorrect_functions: The functions that were incorrect in the lab submission.
    :param incorrect_multiple_choice: The multiple choice questions that were incorrect within this lab.
    :return: A string within information detailing what was incorrect..
    """
    if not incorrect_functions and not incorrect_multiple_choice:
        raise Exception("get_incorrect_report called for perfect lab.")

    message = ""

    if incorrect_functions:
        message += "There were %d incorrect functions:" % len(incorrect_functions) + "\n"
        message += "\tIncorrect functions: " + ", ".join(incorrect_functions) + "\n"

    if incorrect_multiple_choice:
        message += "There were %d incorrect multiple choice answers:" % len(incorrect_multiple_choice) + "\n"
        message += "\tIncorrect multiple choice: " + ", ".join([str(c) for c in incorrect_multiple_choice]) + "\n"

    return message


def print_lab_score(ucid, lab_score, use_short_printout):
    """
    Print out the score for any lab.

    :param ucid: UCID of the lab submitter.
    :param lab_score: The score received on the lab.
    :param use_short_printout: Should defer to shorthand output. If true, will only print in short hand.
    :return: None
    """
    incorrect_functions = lab_score.get_incorrect_functions()
    incorrect_multiple_choice = lab_score.get_incorrect_multiple_choice()

    if use_short_printout or (not incorrect_multiple_choice and not incorrect_functions):
        print("%s received a %d" % (ucid, lab_score.score))
        return

    print_incorrect_box(ucid, get_incorrect_report(incorrect_functions, incorrect_multiple_choice))
