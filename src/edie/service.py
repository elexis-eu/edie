from edie.api import ApiClient
from edie.evaluator import Edie
from edie.model import Dictionary
import uuid

from metrics.entry import FormsPerEntryMetric, AvgDefinitionLengthEvaluator, NumberOfSensesEvaluator, \
    DefinitionOfSenseEvaluator
from metrics.metadata import PublisherEvaluator, LicenseEvaluator, SizeOfDictionaryEvaluator, MetadataQuantityEvaluator, \
    RecencyEvaluator


class EvaluationService(object):
    def evaluate(self, evaluation_id: uuid.UUID, endpoint: str = "http://localhost:8000/", api_key: str = None):
        report = {"endpoint": endpoint, "available": True, "dictionaries": {}}
        api_instance = ApiClient(endpoint, api_key)
        metadata_evaluators = [PublisherEvaluator(), LicenseEvaluator(), MetadataQuantityEvaluator(),
                               RecencyEvaluator(),
                               SizeOfDictionaryEvaluator()]
        entry_evaluators = [FormsPerEntryMetric(), NumberOfSensesEvaluator(), DefinitionOfSenseEvaluator(),
                            AvgDefinitionLengthEvaluator()]
        edie = Edie(api_instance, metadata_metrics_evaluators=metadata_evaluators,
                    entry_metrics_evaluators=entry_evaluators)

        test_dictionaries = [
            "elexis-oeaw-jakob"
        ]
        dictionaries: [Dictionary] = edie.load_dictionaries(test_dictionaries)
        entry_report = edie.evaluate_entries(dictionaries)
        metadata_report = edie.evaluate_metadata(dictionaries)
        merged_report = edie.evaluation_report(entry_report, metadata_report)
        final_report = edie.aggregated_evaluation(merged_report)