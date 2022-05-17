import json
import unittest
import pytest

from edie.model import JsonEntry, Entry
from edie.vocabulary import Vocabulary
from metrics.entry import AvgDefinitionLengthEvaluator, NumberOfSensesEvaluator, SupportedFormatsEvaluator, \
    DefinitionOfSenseEvaluator


@pytest.fixture(scope="class")
def entries_response(request):
    with open("test/data/entries.json") as f:
        loaded_json = json.load(f)
        request.cls.entries_response = JsonEntry(loaded_json)


@pytest.fixture(scope="class")
def entries_metadata(request):
    with open("test/data/lemma_list.json") as f:
        loaded_json = json.load(f)
        request.cls.entries_metadata = Entry(loaded_json[0])


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

            evaluator.accumulate(entry, None)

            self.assertEqual(evaluator.senses_count, 2)
            self.assertGreater(evaluator.total_definition_char_length, 0)
            self.assertEqual(evaluator.total_definition_token_length, 3)
            self.assertEqual(evaluator.entry_count, 1)

    def testResult(self):
        with open("test/data/entries_2_senses.json") as f:
            entry_json = json.load(f)
            entry: JsonEntry = JsonEntry(entry_json)
            evaluator = AvgDefinitionLengthEvaluator()
            evaluator.accumulate(entry, None)

            result = evaluator.result()

        self.assertGreater(result[Vocabulary.DEFINITION_LENGTH_PER_ENTRY_BY_CHARACTER], 0.0)
        self.assertGreater(result[Vocabulary.DEFINITION_LENGTH_PER_ENTRY_BY_TOKEN], 0.0)
        self.assertGreater(result[Vocabulary.DEFINITION_LENGTH_PER_SENSE_BY_CHARACTER], 0.0)
        self.assertGreater(result[Vocabulary.DEFINITION_LENGTH_PER_SENSE_BY_TOKEN], 0.0)

    def testReset(self):
        with open("test/data/entries_2_senses.json") as f:
            entry_json = json.load(f)
            entry: JsonEntry = JsonEntry(entry_json)
            evaluator = AvgDefinitionLengthEvaluator()
            evaluator.accumulate(entry, None)

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

        evaluator.accumulate(entry, None)

        self.assertEqual(evaluator.senses_count, 1)
        self.assertEqual(evaluator.entry_count, 1)


@pytest.mark.usefixtures("entries_response")
@pytest.mark.usefixtures("entries_metadata")
class TestSupportedFormats(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_supported_formats_init(self) -> None:
        evaluator = SupportedFormatsEvaluator()

        self.assertEqual(evaluator.formats_count, 0)
        self.assertEqual(evaluator.entry_count, 0)
        self.assertEqual(evaluator.json_count, 0)
        self.assertEqual(evaluator.tei_count, 0)
        self.assertEqual(evaluator.ontolex_count, 0)

    def test_entry(self) -> None:
        evaluator = SupportedFormatsEvaluator()

        evaluator.accumulate(self.entries_response, self.entries_metadata)

        self.assertEqual(evaluator.entry_count, 1)
        self.assertEqual(evaluator.formats_count, 3)
        self.assertEqual(evaluator.json_count, 1)
        self.assertEqual(evaluator.tei_count, 1)
        self.assertEqual(evaluator.ontolex_count, 1)

    def test_report(self) -> None:
        evaluator = SupportedFormatsEvaluator()
        evaluator.accumulate(self.entries_response, self.entries_metadata)

        result = evaluator.result()

        self.assertEqual(result[Vocabulary.FORMATS_PER_ENTRY], 3)
        self.assertEqual(result[Vocabulary.JSON_SUPPORTED_ENTRIES], 1)
        self.assertEqual(result[Vocabulary.TEI_SUPPORTED_ENTRIES], 1)
        self.assertEqual(result[Vocabulary.ONTOLEX_SUPPORTED_ENTRIES], 1)
        self.assertEqual(result[Vocabulary.JSON_COVERAGE], 1)
        self.assertEqual(result[Vocabulary.TEI_COVERAGE], 1)
        self.assertEqual(result[Vocabulary.ONTOLEX_COVERAGE], 1)

    def test_reset(self):
        evaluator = SupportedFormatsEvaluator()
        evaluator.accumulate(self.entries_response, self.entries_metadata)

        evaluator.reset()

        self.assertEqual(evaluator.entry_count, 0)
        self.assertEqual(evaluator.formats_count, 0)
        self.assertEqual(evaluator.json_count, 0)
        self.assertEqual(evaluator.tei_count, 0)
        self.assertEqual(evaluator.ontolex_count, 0)


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
            evaluator.accumulate(entry, None)

        evaluator.reset()

        self.assertEqual(evaluator.senses_count, 0)
        self.assertEqual(evaluator.definition_count, 0)
        self.assertEqual(evaluator.entry_count, 0)

    def test_result(self) -> None:
        evaluator = DefinitionOfSenseEvaluator()
        with open("test/data/entries.json") as f:
            entry_json = json.load(f)
            entry: JsonEntry = JsonEntry(entry_json)
            evaluator.accumulate(entry, None)

        result = evaluator.result()

        self.assertEqual(result[Vocabulary.DEFINITIONS_PER_SENSE], 1.0)
        self.assertEqual(result[Vocabulary.DEFINITIONS_PER_ENTRY], 1.0)

    def test_entry(self) -> None:
        with open("test/data/entries.json") as f:
            entry_json = json.load(f)
            entry: JsonEntry = JsonEntry(entry_json)
            evaluator = DefinitionOfSenseEvaluator()

            evaluator.accumulate(entry, None)

        self.assertEqual(evaluator.entry_count, 1)
        self.assertEqual(evaluator.senses_count, 1)
        self.assertEqual(evaluator.definition_count, 1)
