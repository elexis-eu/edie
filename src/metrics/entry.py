from edie.model import Entry, JsonEntry
from edie.vocabulary import Vocabulary
from metrics.base import EntryMetric


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
            return {Vocabulary.FORMS_PER_ENTRY: self.form_count / self.entry_count}
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
            result.update({Vocabulary.DEFINITION_LENGTH_PER_ENTRY_BY_CHARACTER: self.total_definition_char_length / self.entry_count})
            result.update({Vocabulary.DEFINITION_LENGTH_PER_ENTRY_BY_TOKEN: self.total_definition_token_length / self.entry_count})

        if self.senses_count > 0:
            result.update(
                {Vocabulary.DEFINITION_LENGTH_PER_SENSE_BY_CHARACTER: self.total_definition_char_length / self.senses_count})
            result.update({Vocabulary.DEFINITION_LENGTH_PER_SENSE_BY_TOKEN: self.total_definition_token_length / self.senses_count})

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
            return {Vocabulary.SENSES_PER_ENTRY: self.senses_count / self.entry_count}
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
            if metadata_format == Vocabulary.JSON_FORMAT:
                self.json_count += 1
            elif metadata_format == Vocabulary.TEI_FORMAT:
                self.tei_count += 1
            elif metadata_format == Vocabulary.ONTOLEX_FORMAT:
                self.ontolex_count += 1

    def result(self) -> dict:
        result = {}
        if self.entry_count > 0:
            result[Vocabulary.FORMATS_PER_ENTRY] = self.formats_count / self.entry_count
            result[Vocabulary.JSON_SUPPORTED_ENTRIES] = self.json_count
            result[Vocabulary.TEI_SUPPORTED_ENTRIES] = self.tei_count
            result[Vocabulary.ONTOLEX_SUPPORTED_ENTRIES] = self.ontolex_count
            result[Vocabulary.JSON_COVERAGE] = self.json_count / self.entry_count
            result[Vocabulary.TEI_COVERAGE] = self.tei_count / self.entry_count
            result[Vocabulary.ONTOLEX_COVERAGE] = self.ontolex_count / self.entry_count

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

    def accumulate(self, entry_details: JsonEntry, entry_metadata=None):
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
            result.update({Vocabulary.DEFINITIONS_PER_SENSE: self.definition_count / self.senses_count})
        if self.entry_count > 0:
            result.update({Vocabulary.DEFINITIONS_PER_ENTRY: self.definition_count / self.entry_count})
        return result
