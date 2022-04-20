from abc import ABC, abstractmethod

from edie.model import Entry


class MetadataMetric(ABC):
    """Abstract class for a metric that depends on only the metadata"""

    @abstractmethod
    def analyze(self, metadata):
        pass

    @abstractmethod
    def result(self):
        pass

    @abstractmethod
    def reset(self):
        pass


class ApiMetric(ABC):
    """Abstract class for a metric that depends on only the metadata"""

    @abstractmethod
    def analyze(self, api_response):
        pass


class ApiMetadataResponseEvaluator(ApiMetric):
    def __init__(self):
        self.dict_count = 0
        self.languages = {}

    def analyze(self, api_response):
        for el in api_response.dictionaries:
            self.dict_count += 1
            if 'language' in api_response.dictionaries[el]:
                lang = api_response.dictionaries[el]['language']
                if lang not in self.languages:
                    self.languages[lang] = 1
                else:
                    self.languages[lang] += 1

    def reset(self):
        self.__init__()

    def result(self):
        if self.dict_count > 0:
            return {"dictionary count": self.dict_count}
        else:
            return {}


class EntryMetric(ABC):
    """Abstract class for a metric that accumulates information by iterating
       over the entries in a dictionary"""

    @abstractmethod
    def accumulate(self, entry_details: object, entry_metadata: Entry) -> None:
        pass

    @abstractmethod
    def result(self) -> dict:
        pass

    @abstractmethod
    def reset(self) -> None:
        pass
