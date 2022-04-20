from edie.vocabulary import SIZE_OF_DICTIONARY
from metrics.base import MetadataMetric


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
