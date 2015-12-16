from libs.finished_manager import FinishedLabHandler

__author__ = "Joshua D. Katz"


class ConsoleOutputManager(FinishedLabHandler):
    def __init__(self, prefer_shorthand):
        self.prefer_shorthand = prefer_shorthand

    def handle_lab(self, lab_score, broken=False):
        printout = lab_score.get_score_report(self.prefer_shorthand)

        print(printout)
