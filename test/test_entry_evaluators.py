import json
import unittest

from edie.model import JsonEntry
from metrics.base import AvgDefinitionLengthEvaluator, NumberOfSensesEvaluator, DefinitionOfSenseEvaluator


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


class TestNumberOfSenses(unittest.TestCase):

    def setUp(self):
        self.numberOfSensesEvaluator: NumberOfSensesEvaluator = NumberOfSensesEvaluator()

    def tearDown(self):
        pass

    def testEntry(self):
        f = open("test/data/entries.json")
        entry_json = json.load(f)
        f.close()

        entry: JsonEntry = JsonEntry(entry_json)  # TODO: should be Entry()

        evaluator = NumberOfSensesEvaluator()

        evaluator.accumulate(entry)

        self.assertEqual(evaluator.senses_count, 1)
        self.assertEqual(evaluator.entry_count, 1)


class TestDefinitionOfSenses(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_definition_of_sense_init(self) -> None:
        evaluator = DefinitionOfSenseEvaluator()

        self.assertEqual(evaluator.senses_count, 0)
        self.assertEqual(evaluator.definition_count, 0)
        self.assertEqual(evaluator.entry_count, 0)

    def test_reset(self) -> None:
        evaluator = DefinitionOfSenseEvaluator()
        with open("test/data/entries.json") as f:
            entry_json = json.load(f)

            entry: JsonEntry = JsonEntry(entry_json)
            evaluator.accumulate(entry)

        evaluator.reset()

        self.assertEqual(evaluator.senses_count, 0)
        self.assertEqual(evaluator.definition_count, 0)
        self.assertEqual(evaluator.entry_count, 0)

    def test_result(self) -> None:
        evaluator = DefinitionOfSenseEvaluator()
        with open("test/data/entries.json") as f:
            entry_json = json.load(f)
            entry: JsonEntry = JsonEntry(entry_json)
            evaluator.accumulate(entry)

        result = evaluator.result()

        self.assertEqual(result['DefinitionPerSense'], 1.0)
        self.assertEqual(result['DefinitionPerEntry'], 1.0)

    def test_entry(self) -> None:
        with open("test/data/entries.json") as f:
            entry_json = json.load(f)
            entry: JsonEntry = JsonEntry(entry_json)
            evaluator = DefinitionOfSenseEvaluator()

            evaluator.accumulate(entry)

        self.assertEqual(evaluator.entry_count, 1)
        self.assertEqual(evaluator.senses_count, 1)
        self.assertEqual(evaluator.definition_count, 1)


