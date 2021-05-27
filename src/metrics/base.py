from abc import ABC, abstractmethod

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


    def accumulate(self, entry):
        self.form_count += 1
        self.form_count += len(entry.other_form)
        self.entry_count += 1

    def result(self):
        if self.entry_count > 0:
            return { "formsPerEntry": self.form_count / self.entry_count }
        else:
            return {}

    def reset(self):
        self.form_count = 0
        self.entry_count = 0
