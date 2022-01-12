from edie.api import ApiClient
from edie.model import Metadata, Dictionary


class Edie(object):
    def __init__(self, api_client):
        self.dictionaries: [Dictionary] = []
        self.lexonomy_client: ApiClient = api_client

    def load_dictionaries(self, dictionaries: [str] = None):
        dictionary_ids = dictionaries if dictionaries is not None else self.lexonomy_client.dictionaries()[
            'dictionaries']
        for dictionary_id in dictionary_ids:
            metadata = Metadata(self.lexonomy_client.about(dictionary_id))
            dictionary = Dictionary(dictionary_id, metadata)
            self.dictionaries.append(dictionary)
        return self.dictionaries
