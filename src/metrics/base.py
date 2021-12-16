from abc import ABC, abstractmethod

from edie.model import Entry, JsonEntry


class MetadataMetric(ABC):
    """Abstract class for a metric that depends on only the metadata"""

    @abstractmethod
    def apply(metadata):
        pass


class EntryMetric(ABC):
    """Abstract class for a metric that accumulates information by iterating
       over the entries in a dictionary"""

    @abstractmethod
    def accumulate(self, entry):
        pass

    @abstractmethod
    def result(self):
        pass

    @abstractmethod
    def reset(self):
        pass


class FormsPerEntryMetric(EntryMetric):
    def __init__(self):
        self.form_count = 0
        self.entry_count = 0

    def accumulate(self, entry: Entry):
        self.form_count += 1
        self.form_count += len(entry.other_form)
        self.entry_count += 1

    def result(self):
        if self.entry_count > 0:
            return {"formsPerEntry": self.form_count / self.entry_count}
        else:
            return {}

    def reset(self):
        self.form_count = 0
        self.entry_count = 0


class AvgDefinitionLengthEvaluator(EntryMetric):
    def __init__(self):
        self.entry_count = 0
        self.total_definition_char_length = 0
        self.total_definition_token_length = 0
        self.senses_count = 0

    def accumulate(self, entry):
        self.entry_count += 1
        self.senses_count += len(entry.senses)

        for sense in entry.senses:
            if 'definition' is not None:
                self.total_definition_char_length += len(sense.definition)
                self.total_definition_token_length += len(sense.definition.split())

    def result(self):
        result = {}
        if self.entry_count > 0:
            result.update({"DefinitionLengthPerEntryByCharacter": self.total_definition_char_length / self.entry_count})
            result.update({"DefinitionLengthPerEntryByToken": self.total_definition_token_length / self.entry_count})

        if self.senses_count > 0:
            result.update({"DefinitionLengthPerSenseByCharacter": self.total_definition_char_length / self.senses_count})
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

    def accumulate(self, entry: JsonEntry):
        self.senses_count += len(entry.senses)
        self.entry_count += 1

    def result(self):
        if self.entry_count > 0:
            return {"sensesPerEntry": self.senses_count / self.entry_count}
        else:
            return {}

    def reset(self):
        self.senses_count = 0
        self.entry_count = 0


class DefinitionOfSenseEvaluator(object):
    def __init__(self):
        self.entry_count = 0
        self.definition_count = 0
        self.senses_count = 0

    def accumulate(self, entry: JsonEntry):
        self.senses_count += len(entry.senses)
        self.entry_count += 1
        for sense in entry.senses:
            if sense.definition is not None:
                self.definition_count += 1

    def reset(self):
        self.entry_count = 0
        self.definition_count = 0
        self.senses_count = 0

    def result(self):
        result = {}
        if self.senses_count > 0:
            result.update({"DefinitionPerSense": self.definition_count / self.senses_count})
        if self.entry_count > 0:
            result.update({"DefinitionPerEntry": self.definition_count / self.entry_count})
        return result

