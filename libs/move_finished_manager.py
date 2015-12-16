from libs.finished_manager import FinishedLabHandler
from os.path import exists, isdir, join, abspath, basename
from os import rename

__author__ = 'Joshua D. Katz'


class MoveFinishedLabHandler(FinishedLabHandler):
    def __init__(self, move_location):
        self.move_location = move_location

    def has_move_location(self):
        return self.move_location is not None and exists(self.move_location) and isdir(self.move_location)

    def get_move_path(self):
        if not self.has_move_location():
            return None
        return abspath(self.move_location)

    def handle_lab(self, lab, broken=False):
        if not self.has_move_location():
            return

        new_location = join(self.get_move_path(), basename(lab.lab_path))

        rename(lab.lab_path, new_location)
