from abc import ABCMeta, abstractmethod

__author__ = 'Joshua D. Katz'


class FinishedLabManager:
    def __init__(self, finished_lab_handlers):
        self.finished_lab_handlers = finished_lab_handlers
        pass

    def has_finished_lab_handlers(self):
        return bool(self.finished_lab_handlers)

    def handle_graded_lab(self, lab_scores):
        if not self.has_finished_lab_handlers():
            return

        for handler in self.finished_lab_handlers:
            handler.handle_labs(lab_scores)


class FinishedLabHandler(metaclass=ABCMeta):
    def handle_labs(self, lab_scores):
        for lab_score in lab_scores:
            self.handle_lab(lab_score, lab_score.is_lab_correct())

    @abstractmethod
    def handle_lab(self, lab_score, broken=False):
        pass
