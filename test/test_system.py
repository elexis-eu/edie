from metrics.base import SizeOfDictionaryEvaluator
from edie.evaluator import Edie
from edie.api import ApiClient
from edie.vocabulary import AGGREGATION_METRICS, DICTIONARY_SIZE
from edie.model import Metadata
from unittest import TestCase

class TestApi(TestCase):
    def setUp(self) -> None:
        self.api_client = ApiClient(endpoint='http://lexonomy.elex.is/', api_key='GXCQJ6S2FZUATM5Z2S0MGZ7XOMXKUFNP')


    def test_aggregated_evaluation_api(self) -> None:
        edie = Edie(self.api_client, metadata_metrics_evaluators=[SizeOfDictionaryEvaluator()])
        edie.load_dictionaries(limit=50)
        edie.evaluate_metadata()

        edie.aggregated_evaluation()
        report = edie.report[AGGREGATION_METRICS][DICTIONARY_SIZE]

        assert ('min' in report)
        assert ('max' in report)
        assert (report['max'] >= report['min'])


    def test_aggregated_evaluation_parametrized(self) -> None:
        sample_dict = 'elexis-kd-arfr'

        about_dict = self.api_client.about(sample_dict)
        metadata = Metadata(about_dict)
        #print(about_dict, dir(about_dict), vars(about_dict))
        if metadata.genre:
            genre = metadata.genre

            edie = Edie(self.api_client, metadata_metrics_evaluators=[SizeOfDictionaryEvaluator()])
            edie.load_dictionaries(limit=50,genre=genre)
            edie.evaluate_metadata()
            edie.aggregated_evaluation()
            report = edie.report[AGGREGATION_METRICS][DICTIONARY_SIZE]

            assert (metadata.entry_count >= report['min'])
