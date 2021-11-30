from abc import ABC, abstractmethod

from src.edie.model import Entry, JsonEntry


class MetadataMetric(ABC):
    """Abstract class for a metric that depends on only the metadata"""

    @abstractmethod
    def analyze(self, metadata):
        pass


class PublisherEvaluator(MetadataMetric):
    def __init__(self):
        self.publisher = ''
        self.publisher_info_present = False

    def analyze(self, metadata):
        if metadata.agent:
            self.publisher = metadata.agent # TODO
            self.publisher_info_present = True

class LicenseEvaluator(MetadataMetric):
    def __init__(self):
        self.license = ''
        self.license_info_present = False

    def analyze(self, metadata):
        if metadata.license:
            self.license = metadata.license
            self.license_info_present = True

class MetadataQuantityEvaluator(MetadataMetric):
    def __init__(self):
        self.metric_count = 0
        self.total_metrics = 0

    def analyze(self, metadata):
        for el in vars(metadata):
            self.total_metrics+=1
            if vars(metadata)[el]!=None:
                self.metric_count+=1

class RecencyEvaluator(MetadataMetric):
    def __init__(self):
        self.recency = None

    def analyze(self, metadata):
        if metadata.issued:
            self.recency = 2021-int(metadata.issued.year)
        elif metadata.created:
            self.recency = 2021 - int(metadata.created.year)


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

    def reset(self):
        self.senses_count = 0
        self.entry_count = 0
