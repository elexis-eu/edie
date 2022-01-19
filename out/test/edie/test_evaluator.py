import json
import unittest
from unittest import TestCase
from unittest.mock import patch

from edie.evaluator import Edie
from edie.model import Dictionary, Metadata, JsonEntry
from metrics.base import AvgDefinitionLengthEvaluator


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

        metadata_report = edie.evaluate_metadata()

        self.assertTrue(self.dict_id in metadata_report)
        self.assertTrue(metadata_report[self.dict_id]['metadataErrors'])

    @patch('metrics.base.RecencyEvaluator')
    def test_metadata_evaluation(self, recency_evaluator):
        recency_evaluator.result.return_value = {'recency': 100}
        dictionary_id = [self.dict_id]
        edie = Edie(self.api_client, metadata_metrics_evaluators=[recency_evaluator])
        edie.load_dictionaries(dictionary_id)

        metadata_report = edie.evaluate_metadata()

        self.assertIsNotNone(metadata_report[self.dict_id]['recency'])

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

            entry_report = edie.evaluate_entries()

            self.assertIsNotNone(entry_report[self.dict_id]['DefinitionLengthPerEntryByCharacter'])
            self.assertIsNotNone(entry_report[self.dict_id]['DefinitionLengthPerEntryByToken'])
            self.assertIsNotNone(entry_report[self.dict_id]['DefinitionLengthPerSenseByCharacter'])
            self.assertIsNotNone(entry_report[self.dict_id]['DefinitionLengthPerSenseByToken'])


class TestDictionarySize(unittest.TestCase):
    def setUp(self):
        self.


class TestAverageDefinitionLength(unittest.TestCase):
    def setUp(self):
        self.avgDefSenseEvaluator: AvgDefinitionLengthEvaluator = AvgDefinitionLengthEvaluator()

    def tearDown(self):
        pass

    def testInit(self):
        evaluator: AvgDefinitionLengthEvaluator = AvgDefinitionLengthEvaluator()

        self.assertEqual(evaluator.senses_count, 0)
        self.assertEqual(evaluator.total_definition_char_length, 0)
        self.assertEqual(evaluator.entry_count, 0)
        self.assertEqual(evaluator.total_definition_token_length, 0)

    def testTwoEntriesAccumulation(self):
        with open("test/data/entries_2_senses.json") as f:
            entry_json = json.load(f)
            entry: JsonEntry = JsonEntry(entry_json)
            evaluator = AvgDefinitionLengthEvaluator()

            evaluator.accumulate(entry)

            self.assertEqual(evaluator.senses_count, 2)
            self.assertGreater(evaluator.total_definition_char_length, 0)
            self.assertEqual(evaluator.total_definition_token_length, 13)
            self.assertEqual(evaluator.entry_count, 1)

    def testResult(self):
        with open("test/data/entries_2_senses.json") as f:
            entry_json = json.load(f)
            entry: JsonEntry = JsonEntry(entry_json)
            evaluator = AvgDefinitionLengthEvaluator()
            evaluator.accumulate(entry)

            result = evaluator.result()

        self.assertGreater(result['DefinitionLengthPerSenseByCharacter'], 0.0)
        self.assertGreater(result['DefinitionLengthPerSenseByToken'], 0.0)
        self.assertGreater(result['DefinitionLengthPerEntryByCharacter'], 0.0)
        self.assertGreater(result['DefinitionLengthPerEntryByToken'], 0.0)

    def testReset(self):
        with open("test/data/entries_2_senses.json") as f:
            entry_json = json.load(f)
            entry: JsonEntry = JsonEntry(entry_json)
            evaluator = AvgDefinitionLengthEvaluator()
            evaluator.accumulate(entry)

            evaluator.reset()

        self.assertEqual(evaluator.entry_count, 0)
        self.assertEqual(evaluator.senses_count, 0)
        self.assertEqual(evaluator.total_definition_token_length, 0)
        self.assertEqual(evaluator.total_definition_char_length, 0)


