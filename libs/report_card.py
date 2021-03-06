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


def get_error_report(ucid, error):
    longest = get_longest_line(error)
    message = get_format_bar(ucid + " lab threw", length=longest) + "\n\n"
    message += error + "\n\n"
    message += get_format_bar("Error will impact grade", length=longest)
    return message


def get_longest_line(string):
    return len(max(string.split("\n"), key=len))


def get_incorrect_report(ucid, score, incorrect_functions, incorrect_multiple_choice):
    """
    Get the message contents to print out for an incorrect lab.

    :param score: The score that the user got.
    :param ucid: The UCID of the user who's grade us being reported.
    :param incorrect_functions: The functions that were incorrect in the lab submission.
    :param incorrect_multiple_choice: The multiple choice questions that were incorrect within this lab.
    :return: A string within information detailing what was incorrect.
    """
    if not incorrect_functions and not incorrect_multiple_choice:
        raise Exception("get_incorrect_report called for perfect lab.")

    message = ""

    if incorrect_functions:
        message += "There were %d incorrect functions:" % len(incorrect_functions) + "\n"
        message += "\n".join(["\t- " + f for f in incorrect_functions]) + "\n"

    if incorrect_multiple_choice:
        message += "There were %d incorrect multiple choice answers:" % len(incorrect_multiple_choice) + "\n"
        message += "\n".join(["\t- Question " + str(c) for c in incorrect_multiple_choice]) + "\n"

    longest = get_longest_line(message)

    if score is not None:
        end = "\n" + get_format_bar("Score is %d" % score, length=longest) + "\n"
    else:
        end = "\n" + get_format_bar("No grade calculated", length=longest) + "\n"

    return get_format_bar(ucid, length=longest) + "\n\n" + message + end
