from edie.api import ApiClient
from edie.model import Metadata, Dictionary
from metrics.base import MetadataMetric


class Edie(object):
    def __init__(self, api_client, metadata_metrics_evaluators: [MetadataMetric] = None):
        self.lexonomy_client: ApiClient = api_client
        self.dictionaries: [Dictionary] = []
        self.metadata_metrics_evaluators: [MetadataMetric] = metadata_metrics_evaluators if metadata_metrics_evaluators is not None else []
        self.metadata_report = {}
        self.report = {"endpoint": api_client.endpoint, "available": True, "dictionaries": {}}

    def load_dictionaries(self, dictionaries: [str] = None):
        correct_dictionaries = [
            "elexis-dsl-kalkar",
            "elexis-dsl-moth",
            "elexis-dsl-ods",
            "elexis-oeaw-jakob",
            "elexis-oeaw-schranka",
            "elexis-tcdh-bmz"
        ]
        dictionary_ids = dictionaries if dictionaries is not None else correct_dictionaries
        for dictionary_id in dictionary_ids:
            metadata = Metadata(self.lexonomy_client.about(dictionary_id))
            dictionary = Dictionary(dictionary_id, metadata)
            self.dictionaries.append(dictionary)
        return self.dictionaries

    def evaluate_metadata(self):
        for dictionary in self.dictionaries:
            metadata_report = {}
            metadata = dictionary.metadata
            if dictionary.metadata.errors:
                metadata_report['metadataErrors'] = metadata.errors

            for metadata_evaluator in self.metadata_metrics_evaluators:
                metadata_evaluator.analyze(metadata)
                metadata_report.update(metadata_evaluator.result())

            self.metadata_report[dictionary.id] = metadata_report

        return self.metadata_report

