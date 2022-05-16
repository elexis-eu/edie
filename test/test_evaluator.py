import json
from unittest import TestCase
from unittest.mock import patch

from edie.evaluator import Edie
from edie.model import Dictionary, Metadata
from edie.vocabulary import *
from metrics.entry import AvgDefinitionLengthEvaluator


class TestEdie(TestCase):
    @staticmethod
    def _entry_request(dict_id, entry_id):
        if dict_id == 'DICT_ID_1':
            with open("test/data/entries.json") as sample:
                return json.load(sample)
        else:
            with open("test/data/entries_2_senses.json") as sample:
                return json.load(sample)

    @staticmethod
    def _list_request(dict_id, limit, offset):
        if dict_id == 'DICT_ID_1':
            with open("test/data/entries_list.json") as sample:
                return json.load(sample)
        else:
            with open("test/data/entries_list_2.json") as sample:
                return json.load(sample)

    @patch('edie.api.ApiClient')
    def setUp(self, api_client) -> None:
        with open('test/data/dictionaries.json') as dictionaries_file, open(
                'test/data/about_with_error.json') as about_file:
            self.dict_id_1 = 'DICT_ID_1'
            self.dict_id_2 = 'DICT_ID_2'
            self.api_client = api_client
            self.api_client.about.return_value = json.load(about_file)
            self.api_client.dictionaries.return_value = json.load(dictionaries_file)
            self.api_client.list.side_effect = self._list_request
            self.api_client.json.side_effect = self._entry_request

    def test_init_edie(self) -> None:
        pass

    def test_load_specific_dictionaries(self):
        dictionary_id = [self.dict_id_1]
        edie = Edie(self.api_client)

        response: [Dictionary] = edie.load_dictionaries(dictionary_id)

        self.api_client.dictionaries.assert_not_called()
        self.api_client.about.assert_called_once_with(self.dict_id_1)
        self.assertEqual(len(response), 1)
        self.assertEqual(len(edie.dictionaries), 1)
        self.assertIsInstance(edie.dictionaries[0], Dictionary)
        self.assertEqual(edie.dictionaries[0].id, self.dict_id_1)

    def test_load_dictionaries(self):
        edie = Edie(self.api_client)

        response: [Dictionary] = edie.load_dictionaries()

        # api_client.dictionaries.assert_called_once()
        self.assertEqual(self.api_client.about.call_count, 2)
        self.assertEqual(len(response), 2)
        self.assertEqual(len(edie.dictionaries), 2)
        self.assertIsInstance(edie.dictionaries[0], Dictionary)

    def test_metadata_with_errors_evaluation(self):
        dictionary_id = [self.dict_id_1]
        edie = Edie(self.api_client)
        edie.load_dictionaries(dictionary_id)

        edie.evaluate_metadata()

        self.assertTrue(self.dict_id_1 in edie.report['dictionaries'])
        self.assertTrue(edie.report['dictionaries'][self.dict_id_1]['metadata_report']['errors'])

    @patch('metrics.metadata.RecencyEvaluator')
    def test_metadata_evaluation(self, recency_evaluator):
        recency_evaluator.result.return_value = {'recency': 100}
        dictionary_id = [self.dict_id_1]
        edie = Edie(self.api_client, metadata_metrics_evaluators=[recency_evaluator])
        edie.load_dictionaries(dictionary_id)

        edie.evaluate_metadata()

        self.assertIsNotNone(edie.report['dictionaries'][self.dict_id_1]['metadata_report']['recency'])

    @patch('metrics.entry.AvgDefinitionLengthEvaluator')
    def test_entry_evaluation(self, avg_def_evaluator):
        with open('test/data/about_with_error.json') as about_file:
            metadata_json = json.load(about_file)

            avg_def_evaluator.result.return_value = {DEFINITION_LENGTH_PER_ENTRY_BY_CHARACTER: 71.0,
                                                     DEFINITION_LENGTH_PER_ENTRY_BY_TOKEN: 13.0,
                                                     DEFINITION_LENGTH_PER_SENSE_BY_CHARACTER: 35.5,
                                                     DEFINITION_LENGTH_PER_SENSE_BY_TOKEN: 6.5}
            edie = Edie(self.api_client, entry_metrics_evaluators=[avg_def_evaluator])
            edie.dictionaries = [Dictionary('DICT_ID_1', metadata=Metadata(metadata_json))]

            edie.evaluate_entries()

            self.assertIsNotNone(edie.entry_report(self.dict_id_1)[DEFINITION_LENGTH_PER_ENTRY_BY_CHARACTER])
            self.assertIsNotNone(edie.entry_report(self.dict_id_1)[DEFINITION_LENGTH_PER_ENTRY_BY_TOKEN])
            self.assertIsNotNone(edie.entry_report(self.dict_id_1)[DEFINITION_LENGTH_PER_SENSE_BY_CHARACTER])
            self.assertIsNotNone(edie.entry_report(self.dict_id_1)[DEFINITION_LENGTH_PER_SENSE_BY_TOKEN])

    @patch('metrics.entry.AvgDefinitionLengthEvaluator')
    def test_entry_evaluation_with_errors(self, avg_def_evaluator):
        with open('test/data/about_with_error.json') as about_file:
            metadata_json = json.load(about_file)
            self.api_client.list.return_value = "Not Json"

            edie = Edie(self.api_client, entry_metrics_evaluators=[avg_def_evaluator])
            edie.dictionaries = [Dictionary('DICT_ID_1', metadata=Metadata(metadata_json))]

            edie.evaluate_entries()

            self.assertIsNotNone(edie.entry_report(self.dict_id_1)['errors'])
            self.assertIs(len(edie.entry_report(self.dict_id_1)['errors']), 5)

    def test_entry_evluation_two_dictionaries(self):
        with open('test/data/about_with_error.json') as about_file:
            metadata_json = json.load(about_file)
            edie = Edie(self.api_client, entry_metrics_evaluators=[AvgDefinitionLengthEvaluator()])
            edie.dictionaries = [Dictionary('DICT_ID_1', metadata=Metadata(metadata_json)),
                                 Dictionary('DICT_ID_2', metadata=Metadata(metadata_json))]

            edie.evaluate_entries()

            self.assertEqual(edie.entry_report(self.dict_id_1)[DEFINITION_LENGTH_PER_ENTRY_BY_CHARACTER], 4)
            self.assertIsNotNone(edie.entry_report(self.dict_id_1)[DEFINITION_LENGTH_PER_ENTRY_BY_TOKEN], 1)
            self.assertIsNotNone(edie.entry_report(self.dict_id_1)[DEFINITION_LENGTH_PER_SENSE_BY_CHARACTER], 4)
            self.assertIsNotNone(edie.entry_report(self.dict_id_1)[DEFINITION_LENGTH_PER_SENSE_BY_TOKEN], 1)
            self.assertEqual(edie.entry_report(self.dict_id_2)[DEFINITION_LENGTH_PER_ENTRY_BY_CHARACTER], 14)
            self.assertIsNotNone(edie.entry_report(self.dict_id_2)[DEFINITION_LENGTH_PER_ENTRY_BY_TOKEN], 3)
            self.assertIsNotNone(edie.entry_report(self.dict_id_2)[DEFINITION_LENGTH_PER_SENSE_BY_CHARACTER], 7)
            self.assertIsNotNone(edie.entry_report(self.dict_id_2)[DEFINITION_LENGTH_PER_SENSE_BY_TOKEN], 1.5)

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
        with open("test/data/end_report.json") as report_file:
            end_report = json.load(report_file)
            edie = Edie(self.api_client)
            edie.report = end_report

            df = edie.metadata_evaluation_report_as_dataframe()

            self.assertEqual(len(df.index), 6)
            self.assertEqual(len(df.columns), 4)
            self.assertIn('elexis-dsl-kalkar', df.index)
            self.assertIn('errors', df.columns)
            self.assertIn('total metrics', df.columns)

    def test_aggregation(self) -> None:
        with open("test/data/end_report.json") as report_file:
            end_report = json.load(report_file)
            edie = Edie(self.api_client)
            edie.report = end_report

            edie.aggregated_evaluation()

            self.assertIsNotNone(edie.report[AGGREGATION_METRICS])
            self.assertGreater(edie.report[AGGREGATION_METRICS][DICTIONARY_SIZE]['min'], 0)
            self.assertGreater(edie.report[AGGREGATION_METRICS][DICTIONARY_SIZE]['max'], 0)
            self.assertGreater(edie.report[AGGREGATION_METRICS][DICTIONARY_SIZE]['mean'], 0)
            self.assertGreater(edie.report[AGGREGATION_METRICS][DICTIONARY_SIZE]['median'], 0)
