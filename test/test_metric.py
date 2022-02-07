from abc import ABC
from unittest import TestCase


class AggregatedMetric(ABC):
    pass


class DictionarySizeAggregatedEvaluator(AggregatedMetric):

    def test_aggregatedMetrics(self) -> None:
        evaluator = DictionarySizeAggregatedEvaluator()
        #metric_evaluation_result = edie.report
