import json
import os
import sys
from datetime import datetime

from edie.api import ApiClient
from edie.evaluator import Edie
from edie.model import Dictionary
import uuid

from metrics.entry import FormsPerEntryMetric, AvgDefinitionLengthEvaluator, NumberOfSensesEvaluator, \
    DefinitionOfSenseEvaluator
from metrics.metadata import PublisherEvaluator, LicenseEvaluator, SizeOfDictionaryEvaluator, MetadataQuantityEvaluator, \
    RecencyEvaluator


class EvaluationService(object):
    def __init__(self):
        self.save_path = 'results/'

    def evaluate(self, evaluation_id: uuid.UUID, endpoint: str = "http://localhost:8000/", api_key: str = None):
        sys.stdout.write('Starting evaluation...')
        sys.stdout.flush()

        api_instance = ApiClient(endpoint, api_key)
        metadata_evaluators = [PublisherEvaluator(), LicenseEvaluator(), MetadataQuantityEvaluator(),
                               RecencyEvaluator(),
                               SizeOfDictionaryEvaluator()]
        entry_evaluators = [FormsPerEntryMetric(), NumberOfSensesEvaluator(), DefinitionOfSenseEvaluator(),
                            AvgDefinitionLengthEvaluator()]

        edie = Edie(api_instance, metadata_metrics_evaluators=metadata_evaluators,
                    entry_metrics_evaluators=entry_evaluators)

        #test_dictionaries = ["elexis-oeaw-schranka"]
        dictionaries: [Dictionary] = edie.load_dictionaries(test_dictionaries)
        metadata_report = edie.evaluate_metadata(dictionaries)
        entry_report = edie.evaluate_entries(dictionaries)
        merged_report = edie.evaluation_report(entry_report, metadata_report)
        final_report = edie.aggregated_evaluation(merged_report)

        sys.stderr.write('Writing to file...')
        sys.stderr.flush()
        datetime_postfix = datetime.now().strftime("%y%m%d%H%M%S")
        filename = self.save_path + str(evaluation_id) + '_' + datetime_postfix + '.json'
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w') as f:
            json.dump(final_report, f)

        sys.stdout.write('Evaluation complete.')
        sys.stdout.flush()
