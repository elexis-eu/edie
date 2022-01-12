from edie.api import ApiClient
from edie.model import Metadata, Dictionary


class Edie(object):
    def __init__(self, api_client):
        self.dictionaries: [Dictionary] = []
        self.lexonomy_client: ApiClient = api_client
        self.report = {"endpoint": api_client.endpoint, "available": True, "dictionaries": {}}
        
    def load_dictionaries(self, dictionaries: [str] = None):
        dictionary_ids = dictionaries if dictionaries is not None else self.lexonomy_client.dictionaries()[
            'dictionaries']
        for dictionary_id in dictionary_ids:
            metadata = Metadata(self.lexonomy_client.about(dictionary_id))
            dictionary = Dictionary(dictionary_id, metadata)
            self.dictionaries.append(dictionary)
        return self.dictionaries

    def evaluate_metadata(self):
        for dictionary in self.dictionaries:
            if dictionary.metadata.errors:
            dict_report["metadataErrors"] = metadata.errors
        else:
            for metadata_metric in metadata_metrics:
                dict_report.update(metadata_metric.apply(metadata))

        return metadata

