from edie.evaluator import Edie
from edie.model import Dictionary
import uuid


class EvaluationService(object):
    def __init__(self, edie: Edie):
        self.edie = edie

    def evaluate(self, evaluation_id: uuid.UUID):
        test_dictionaries = [
            "elexis-oeaw-jakob"
        ]
        self.edie.load_dictionaries(test_dictionaries)
        self.edie.evaluate_metadata()
        self.edie.evaluate_entries()
        self.edie.aggregated_evaluation()
        report = self.edie.evaluation_report()
