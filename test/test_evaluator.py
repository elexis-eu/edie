import json
from unittest import TestCase
from unittest.mock import patch

from edie.evaluator import Edie
from edie.model import Dictionary


class TestEdie(TestCase):
    def test_init_edie(self):
        pass

    @patch('edie.api.ApiClient')
    def test_load_specific_dictionaries(self, api_client):
        with open('test/data/about_with_error.json') as about_file:
            dict_id = 'DICT_ID_1'
            api_client.about.return_value = json.load(about_file)
            dictionary_id = [dict_id]
            edie = Edie(api_client)

            response: [Dictionary] = edie.load_dictionaries(dictionary_id)

            api_client.dictionaries.assert_not_called()
            api_client.about.assert_called_once_with(dict_id)
            self.assertEqual(len(response), 1)
            self.assertEqual(len(edie.dictionaries), 1)
            self.assertIsInstance(edie.dictionaries[0], Dictionary)
            self.assertEqual(edie.dictionaries[0].id, dict_id)

    @patch('edie.api.ApiClient')
    def test_load_dictionaries(self, api_client):
        with open('test/data/dictionaries.json') as dictionaries_file, open(
                'test/data/about_with_error.json') as about_file:
            api_client.dictionaries.return_value = json.load(dictionaries_file)
            api_client.about.return_value = json.load(about_file)
            edie = Edie(api_client)

            response: [Dictionary] = edie.load_dictionaries()

            # api_client.dictionaries.assert_called_once()
            self.assertEqual(api_client.about.call_count, 6)
            self.assertEqual(len(response), 6)
            self.assertEqual(len(edie.dictionaries), 6)
            self.assertIsInstance(edie.dictionaries[0], Dictionary)

    @patch('edie.api.ApiClient')
    def test_metadata_with_errors_evaluation(self, api_client):
        with open('test/data/about_with_error.json') as about_file:
            dict_id = 'DICT_ID_1'
            api_client.about.return_value = json.load(about_file)
            dictionary_id = [dict_id]
            edie = Edie(api_client)
            edie.load_dictionaries(dictionary_id)

            metadata_report = edie.evaluate_metadata()

            self.assertTrue(dict_id in metadata_report)
            self.assertTrue(metadata_report[dict_id]['metadataErrors'])

    @patch('edie.api.ApiClient')
    @patch('metrics.base.RecencyEvaluator')
    def test_metadata_evaluation(self, api_client, recency_evaluator):
        with open('test/data/about_with_error.json') as about_file:
            dict_id = 'DICT_ID_1'
            api_client.about.return_value = json.load(about_file)
            recency_evaluator.result.return_value = {'recency': 100}
            dictionary_id = [dict_id]
            edie = Edie(api_client, metadata_metrics_evaluators=[recency_evaluator])
            edie.load_dictionaries(dictionary_id)

            metadata_report = edie.evaluate_metadata()

            self.assertIsNotNone(metadata_report[dict_id]['recency'])
