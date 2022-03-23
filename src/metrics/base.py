from abc import ABC, abstractmethod

from edie.model import Entry, JsonEntry
from edie.vocabulary import SIZE_OF_DICTIONARY, JSON_FORMAT, TEI_FORMAT, ONTOLEX_FORMAT, FORMATS_PER_ENTRY, \
    JSON_SUPPORTED_ENTRIES, TEI_SUPPORTED_ENTRIES, ONTOLEX_SUPPORTED_ENTRIES, JSON_COVERAGE, TEI_COVERAGE, \
    ONTOLEX_COVERAGE


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


class PublisherEvaluator(MetadataMetric):
    def __init__(self):
        self.publisher = ''
        self.publisher_info_present = False

    def analyze(self, metadata):

        if metadata.agent:
            self.publisher = metadata.agent  # TODO
            self.publisher_info_present = True

    def reset(self):
        self.__init__()

    def result(self):
        if self.publisher_info_present:
            return {"publisher": self.publisher}
        else:
            return {}


class LicenseEvaluator(MetadataMetric):
    def __init__(self):
        self.license = ''
        self.license_info_present = False

    def analyze(self, metadata):
        if metadata.license:
            self.license = metadata.license
            self.license_info_present = True

    def reset(self):
        self.__init__()

    def result(self):
        if self.license_info_present:
            return {"license": self.license}
        else:
            return {}


class MetadataQuantityEvaluator(MetadataMetric):
    def __init__(self):
        self.metric_count = 0
        self.total_metrics = 0

    def analyze(self, metadata):
        for el in vars(metadata):
            self.total_metrics += 1
            if vars(metadata)[el] != None:
                self.metric_count += 1

    def reset(self):
        self.__init__()

    def result(self):
        result = {}
        if self.metric_count > 0:
            result["metric count"] = self.metric_count
        if self.total_metrics > 0:
            result["total metrics"] = self.total_metrics
        return result


class RecencyEvaluator(MetadataMetric):
    def __init__(self):
        self.recency = None

    def analyze(self, metadata):
        if metadata.issued:
            self.recency = 2021 - int(metadata.issued.year)
        elif metadata.created:
            self.recency = 2021 - int(metadata.created.year)

    def reset(self):
        self.recency = None

    def result(self):
        if self.recency:
            return {"recency": self.recency}
        else:
            return {}


class ApiMetric(ABC):
    """Abstract class for a metric that depends on only the metadata"""

    @abstractmethod
    def analyze(self, api_response):
        pass


class LexonomyAboutDictEvaluator(ApiMetric):
    def __init__(self):
        self.metrics = 0
        self.target_language = None
        self.source_language = None
        self.genre = None
        self.title = None

    def analyze(self, api_response):


        self.genre = api_response.genre

        self.title = api_response.title

        #if api_response.source_language!='null':
        self.source_language = api_response.source_language

        #if api_response.target_language!='null':
        self.target_language = api_response.target_language


        for el in vars(api_response):
            if vars(api_response)[el] != None:
                self.metrics += 1


    def reset(self):
        self.metrics = 0
        self.target_language = None
        self.source_language = None

    def result(self):
        result = {}
        if self.title:
            result['title'] = self.title
        if self.genre:
            result['genre'] = self.genre
        if self.source_language:
            result['source language'] = self.source_language
        if self.target_language:
            result['target language'] = self.target_language
        if self.metrics > 0:
            result['total metric count'] = self.metrics

        return result





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


class FormsPerEntryMetric(EntryMetric):
    def __init__(self):
        self.form_count = 0
        self.entry_count = 0

    def accumulate(self, entry_details: Entry, entry_metadata):
        self.form_count += 1
        self.form_count += len(entry_details.other_form)
        self.entry_count += 1

    def result(self):
        if self.entry_count > 0:
            return {"formsPerEntry": self.form_count / self.entry_count}
        else:
            return {}

    def reset(self):
        self.__init__()


class AvgDefinitionLengthEvaluator(EntryMetric):
    def __init__(self):
        self.entry_count = 0
        self.total_definition_char_length = 0
        self.total_definition_token_length = 0
        self.senses_count = 0

    def accumulate(self, entry_details, entry_metadata):
        self.entry_count += 1
        self.senses_count += len(entry_details.senses)

        for sense in entry_details.senses:
            if sense.definition is not None:
                self.total_definition_char_length += len(sense.definition)
                self.total_definition_token_length += len(sense.definition.split())

    def result(self):
        result = {}
        if self.entry_count > 0:
            result.update({"DefinitionLengthPerEntryByCharacter": self.total_definition_char_length / self.entry_count})
            result.update({"DefinitionLengthPerEntryByToken": self.total_definition_token_length / self.entry_count})

        if self.senses_count > 0:
            result.update(
                {"DefinitionLengthPerSenseByCharacter": self.total_definition_char_length / self.senses_count})
            result.update({"DefinitionLengthPerSenseByToken": self.total_definition_token_length / self.senses_count})

        return result

    def reset(self):
        self.total_definition_char_length = 0
        self.total_definition_token_length = 0
        self.entry_count = 0
        self.senses_count = 0


class NumberOfSensesEvaluator(EntryMetric):
    def __init__(self):
        self.senses_count = 0
        self.entry_count = 0

    def accumulate(self, entry_details: JsonEntry, entry_metadata):
        self.senses_count += len(entry_details.senses)
        self.entry_count += 1

    def result(self):
        if self.entry_count > 0:
            return {"sensesPerEntry": self.senses_count / self.entry_count}
        else:
            return {}

    def reset(self):
        self.__init__()


class SupportedFormatsEvaluator(EntryMetric):
    def __init__(self):
        self.json_count = 0
        self.tei_count = 0
        self.ontolex_count = 0
        self.entry_count = 0
        self.formats_count = 0

    def accumulate(self, entry_details: object, entry_metadata: Entry):
        self.formats_count += len(entry_metadata.formats)
        self.entry_count += 1
        for metadata_format in entry_metadata.formats:
            if metadata_format == JSON_FORMAT:
                self.json_count += 1
            elif metadata_format == TEI_FORMAT:
                self.tei_count += 1
            elif metadata_format == ONTOLEX_FORMAT:
                self.ontolex_count += 1

    def result(self) -> dict:
        result = {}
        if self.entry_count > 0:
            result[FORMATS_PER_ENTRY] = self.formats_count / self.entry_count
            result[JSON_SUPPORTED_ENTRIES] = self.json_count
            result[TEI_SUPPORTED_ENTRIES] = self.tei_count
            result[ONTOLEX_SUPPORTED_ENTRIES] = self.ontolex_count
            result[JSON_COVERAGE] = self.json_count / self.entry_count
            result[TEI_COVERAGE] = self.tei_count / self.entry_count
            result[ONTOLEX_COVERAGE] = self.ontolex_count / self.entry_count

        return result

    def reset(self):
        self.entry_count = 0
        self.formats_count = 0
        self.json_count = 0
        self.tei_count = 0
        self.ontolex_count = 0


class DefinitionOfSenseEvaluator(EntryMetric):
    def __init__(self):
        self.entry_count = 0
        self.definition_count = 0
        self.senses_count = 0

    def accumulate(self, entry_details: JsonEntry, entry_metadata):
        self.senses_count += len(entry_details.senses)
        self.entry_count += 1
        for sense in entry_details.senses:
            if sense.definition is not None:
                self.definition_count += 1

    def reset(self):
        self.__init__()

    def result(self):
        result = {}
        if self.senses_count > 0:
            result.update({"DefinitionPerSense": self.definition_count / self.senses_count})
        if self.entry_count > 0:
            result.update({"DefinitionPerEntry": self.definition_count / self.entry_count})
        return result


class SizeOfDictionaryEvaluator(MetadataMetric):
    def __init__(self):
        self.avg_size = None
        self.entry_count = None

    def analyze(self, metadata):
        self.entry_count = metadata.entry_count

    def reset(self):
        self.entry_count = None

    def result(self):
        result = {}
        if self.entry_count > 0:
            result.update({SIZE_OF_DICTIONARY: self.entry_count})

        return result
