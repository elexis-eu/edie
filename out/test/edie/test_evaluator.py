import json
from unittest import TestCase
from unittest.mock import patch

from edie.evaluator import Edie
from edie.model import Dictionary, Metadata


class TestEdie(TestCase):
    @patch('edie.api.ApiClient')
    def setUp(self, api_client) -> None:
        with open('test/data/dictionaries.json') as dictionaries_file, open(
                'test/data/about_with_error.json') as about_file:
            self.dict_id = 'DICT_ID_1'
            self.api_client = api_client
            self.api_client.about.return_value = json.load(about_file)
            self.api_client.dictionaries.return_value = json.load(dictionaries_file)

    def test_init_edie(self) -> None:
        pass

    def test_load_specific_dictionaries(self):
        dictionary_id = [self.dict_id]
        edie = Edie(self.api_client)

        response: [Dictionary] = edie.load_dictionaries(dictionary_id)

        self.api_client.dictionaries.assert_not_called()
        self.api_client.about.assert_called_once_with(self.dict_id)
        self.assertEqual(len(response), 1)
        self.assertEqual(len(edie.dictionaries), 1)
        self.assertIsInstance(edie.dictionaries[0], Dictionary)
        self.assertEqual(edie.dictionaries[0].id, self.dict_id)

    def test_load_dictionaries(self):
        edie = Edie(self.api_client)

        response: [Dictionary] = edie.load_dictionaries()

        # api_client.dictionaries.assert_called_once()
        self.assertEqual(self.api_client.about.call_count, 6)
        self.assertEqual(len(response), 6)
        self.assertEqual(len(edie.dictionaries), 6)
        self.assertIsInstance(edie.dictionaries[0], Dictionary)

    def test_metadata_with_errors_evaluation(self):
        dictionary_id = [self.dict_id]
        edie = Edie(self.api_client)
        edie.load_dictionaries(dictionary_id)

        edie.evaluate_metadata()

        self.assertTrue(self.dict_id in edie.report['dictionaries'])
        self.assertTrue(edie.report['dictionaries'][self.dict_id]['metadata_report']['errors'])

    @patch('metrics.base.RecencyEvaluator')
    def test_metadata_evaluation(self, recency_evaluator):
        recency_evaluator.result.return_value = {'recency': 100}
        dictionary_id = [self.dict_id]
        edie = Edie(self.api_client, metadata_metrics_evaluators=[recency_evaluator])
        edie.load_dictionaries(dictionary_id)

        edie.evaluate_metadata()

        self.assertIsNotNone(edie.report['dictionaries'][self.dict_id]['metadata_report']['recency'])

    @patch('metrics.base.AvgDefinitionLengthEvaluator')
    def test_entry_evaluation(self, avg_def_evaluator):
        with open('test/data/about_with_error.json') as about_file:
            metadata_json = json.load(about_file)

            avg_def_evaluator.result.return_value = {'DefinitionLengthPerEntryByCharacter': 71.0,
                                                     'DefinitionLengthPerEntryByToken': 13.0,
                                                     'DefinitionLengthPerSenseByCharacter': 35.5,
                                                     'DefinitionLengthPerSenseByToken': 6.5}
            edie = Edie(self.api_client, entry_metrics_evaluators=[avg_def_evaluator])
            edie.dictionaries = [Dictionary('DICT_ID_1', metadata=Metadata(metadata_json))]

            edie.evaluate_entries()

            self.assertIsNotNone(edie.entry_report(self.dict_id)['DefinitionLengthPerEntryByCharacter'])
            self.assertIsNotNone(edie.entry_report(self.dict_id)['DefinitionLengthPerEntryByToken'])
            self.assertIsNotNone(edie.entry_report(self.dict_id)['DefinitionLengthPerSenseByCharacter'])
            self.assertIsNotNone(edie.entry_report(self.dict_id)['DefinitionLengthPerSenseByToken'])

    @patch('metrics.base.AvgDefinitionLengthEvaluator')
    def test_entry_evaluation_with_errors(self, avg_def_evaluator):
        with open('test/data/about_with_error.json') as about_file:
            metadata_json = json.load(about_file)
            self.api_client.list.return_value = "Not Json"

            edie = Edie(self.api_client, entry_metrics_evaluators=[avg_def_evaluator])
            edie.dictionaries = [Dictionary('DICT_ID_1', metadata=Metadata(metadata_json))]

            edie.evaluate_entries()

            self.assertIsNotNone(edie.entry_report(self.dict_id)['errors'])
            self.assertIs(len(edie.entry_report(self.dict_id)['errors']), 24)

    def test_entry_report_to_dataframe(self):
        with open("test/data/end_report.json") as report_file:
            end_report = json.load(report_file)
            edie = Edie(self.api_client)
            edie.report = end_report

            df = edie.entry_evaluation_report_as_dataframe()

            self.assertEqual(len(df.index), 6)
            self.assertEqual(len(df.columns), 9)
            self.assertIn('elexis-dsl-kalkar', df.index)
            self.assertIn('errors', df.columns)
            self.assertIn('formsPerEntry', df.columns)

    def test_metadata_report_to_dataframe(self):
        