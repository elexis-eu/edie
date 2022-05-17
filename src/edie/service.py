import json
import os
import sys
from pathlib import Path

from edie.api import ApiClient
from edie.evaluator import Edie
from edie.model import Dictionary
import uuid

from metrics.entry import FormsPerEntryMetric, AvgDefinitionLengthEvaluator, NumberOfSensesEvaluator, \
    DefinitionOfSenseEvaluator
from metrics.metadata import LicenseEvaluator, SizeOfDictionaryEvaluator, MetadataQuantityEvaluator, \
    RecencyEvaluator


class EvaluationService(object):
    def __init__(self):
        self.save_path = 'results/'

    def evaluate(self, evaluation_id: uuid.UUID, endpoint: str = "http://localhost:8000/", api_key: str = None):
        sys.stdout.write('Starting evaluation...')
        sys.stdout.flush()

        api_instance = ApiClient(endpoint, api_key)
        metadata_evaluators = [LicenseEvaluator(), MetadataQuantityEvaluator(),
                               RecencyEvaluator(),
                               SizeOfDictionaryEvaluator()]
        entry_evaluators = [FormsPerEntryMetric(), NumberOfSensesEvaluator(), DefinitionOfSenseEvaluator(),
                            AvgDefinitionLengthEvaluator()]

        edie = Edie(api_instance, metadata_metrics_evaluators=metadata_evaluators,
                    entry_metrics_evaluators=entry_evaluators)

        dictionaries: [Dictionary] = edie.load_dictionaries()
        metadata_report = edie.evaluate_metadata(dictionaries)
        entry_report = edie.evaluate_entries(dictionaries)
        merged_report = edie.evaluation_report(entry_report, metadata_report)
        final_report = edie.aggregated_evaluation(merged_report)
        sys.stderr.write('Writing to file...')
        sys.stderr.flush()
        filename = self.save_path + str(evaluation_id) + '.json'
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        with open(filename, 'w') as f:
            json.dump({'evaluation_id': str(evaluation_id), 'result': final_report}, f)

        sys.stdout.write('Evaluation complete.')
        sys.stdout.flush()

    def get_evaluations(self):
        evaluations = []
        paths = sorted(Path(self.save_path).iterdir(), key=os.path.getmtime, reverse=True)
        for p in paths:
            with open(p, 'r') as f:
                evaluations.append(json.load(f))

        return evaluations

    def get_evaluation(self, evaluation_id):
        for evaluation in self.get_evaluations():
            if evaluation['evaluation_id'] == evaluation_id:
                return evaluation['result']
        return None

    def get_dictionary_evaluation(self, evaluation_id, dictionary_id):
        if dictionary_id not in self.get_evaluation(evaluation_id)['dictionaries'].keys():
            return None
        return self.get_evaluation(evaluation_id)['dictionaries'][dictionary_id]
