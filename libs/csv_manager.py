from libs.finished_manager import FinishedLabHandler
from os.path import exists, isfile

__author__ = 'Joshua D. Katz'


class CSVManager(FinishedLabHandler):
    def __init__(self, csv_file, lab_number):

        self.database = {}
        self.lab_number = lab_number

        if exists(csv_file) and isfile(csv_file):
            with open(csv_file) as database:
                for line in database:
                    parts = line.split(",")
                    self.database[parts[0]] = [p.strip() for p in parts[1:]]

        self.file = csv_file

    def handle_labs(self, lab_scores):

        if self.file is None or self.file == "":
            return

        for ucid in self.database:
            ucid_db = self.database[ucid]

            db_size = len(ucid_db)
            if db_size >= self.lab_number:
                continue

            self.database[ucid] = [ucid_db[x] if x < db_size else None for x in range(self.lab_number)]

        for lab in lab_scores:
            if lab.ucid not in self.database:
                self.database[lab.ucid] = [None for x in range(lab.lab_number)]

            self.database[lab.ucid][lab.lab_number - 1] = lab.score if lab.score is not None else -1

        with open(self.file, "w") as csv:
            db = self.database
            for ucid in self.database:
                csv.write("%s,%s\n" % (ucid, ",".join([str(score) if score is not None else "" for score in db[ucid]])))

    def handle_lab(self, lab, broken=False):
        return
