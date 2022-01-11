"""
    ELEXIS Protocol for accessing dictionaries

    This protocol allows data to be shared with the ELEXIS platform and should be implemented by all providers of data to the ELEXIS platform. This is an OpenAPI documentation, for more details about using this specification, please refer to OpenAPI documentations: https://swagger.io/resources/articles/documenting-apis-with-swagger/  # noqa: E501

    The version of the OpenAPI document: 1.0
    Generated by: https://openapi-generator.tech
"""

import sys
import unittest
import json

from edie.model import JsonEntry, Metadata, Entry, JsonApiResponse
from metrics.base import NumberOfSensesEvaluator, PublisherEvaluator, LicenseEvaluator, MetadataQuantityEvaluator, RecencyEvaluator, ApiMetadataResponseEvaluator, DefinitionOfSenseEvaluator, LexonomyAboutDictEvaluator
from metrics.base import NumberOfSensesEvaluator, PublisherEvaluator, LicenseEvaluator, MetadataQuantityEvaluator, RecencyEvaluator, ApiMetadataResponseEvaluator, DefinitionOfSenseEvaluator,AvgDefinitionLengthEvaluator

class TestEntry(unittest.TestCase):
    """Entry unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testEntry(self):
        """Test Entry"""
        # FIXME: construct object with mandatory attributes with example values
        # model = Entry()  # noqa: E501
        pass


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
        f = open("test/data/entries.json")
        entry_json = json.load(f)
        f.close()
        entry: JsonEntry = JsonEntry(entry_json)
        evaluator.accumulate(entry)

        evaluator.reset()

        self.assertEqual(evaluator.senses_count, 0)
        self.assertEqual(evaluator.definition_count, 0)
        self.assertEqual(evaluator.entry_count, 0)

    def test_result(self) -> None:
        evaluator = DefinitionOfSenseEvaluator()
        f = open("test/data/entries.json")
        entry_json = json.load(f)
        f.close()
        entry: JsonEntry = JsonEntry(entry_json)
        evaluator.accumulate(entry)

        result = evaluator.result()

        self.assertEqual(result['DefinitionPerSense'], 1.0)
        self.assertEqual(result['DefinitionPerEntry'], 1.0)

    def test_entry(self) -> None:
            f = open("test/data/entries.json")
            entry_json = json.load(f)
            f.close()
            entry: JsonEntry = JsonEntry(entry_json)
            evaluator = DefinitionOfSenseEvaluator()

            evaluator.accumulate(entry)

            self.assertEqual(evaluator.entry_count, 1)
            self.assertEqual(evaluator.senses_count, 1)
            self.assertEqual(evaluator.definition_count, 1)


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
        f = open("test/data/entries_2_senses.json")
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
        f = open("test/data/entries_2_senses.json")
        entry_json = json.load(f)
        entry: JsonEntry = JsonEntry(entry_json)
        evaluator = AvgDefinitionLengthEvaluator()
        evaluator.accumulate(entry)

        result = evaluator.reset()

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

        entry: JsonEntry = JsonEntry(entry_json) # TODO: should be Entry()

        evaluator = NumberOfSensesEvaluator()

        evaluator.accumulate(entry)

        self.assertEqual(evaluator.senses_count, 1)
        self.assertEqual(evaluator.entry_count, 1)


class TestPublisherMetadata(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_publisher_metadata_init(self) -> None:
        evaluator = PublisherEvaluator()
        self.assertEqual(evaluator.publisher,'')
        self.assertFalse(evaluator.publisher_info_present)


    def test_reset(self) -> None:
        evaluator = PublisherEvaluator()
        f = open("test/data/sample.json")
        entry_json = json.load(f)
        f.close()
        metadata_entry: Metadata = Metadata(entry_json)
        evaluator.analyze(metadata_entry)

        evaluator.reset()

        self.assertEqual(evaluator.publisher, '')
        self.assertFalse(evaluator.publisher_info_present)

    def test_result(self) -> None:
        f = open("test/data/sample.json")
        entry_json = json.load(f)
        f.close()

        metadata_entry: Metadata = Metadata(entry_json)

        evaluator = PublisherEvaluator()
        evaluator.analyze(metadata_entry)
        result = evaluator.result()
        self.assertIsNotNone(result['publisher'])


    def test_entry(self) -> None:
        f = open("test/data/sample.json")
        entry_json = json.load(f)
        f.close()

        metadata_entry: Metadata = Metadata(entry_json)

        evaluator = PublisherEvaluator()
        evaluator.analyze(metadata_entry)
        self.assertTrue(evaluator.publisher_info_present, 'Publisher info missing')


class TestLicence(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_license_init(self) -> None:
        evaluator = LicenseEvaluator()
        self.assertEqual(evaluator.license, '')
        self.assertFalse(evaluator.license_info_present)

    def test_reset(self) -> None:
        f = open("test/data/sample.json")
        entry_json = json.load(f)
        f.close()

        metadata_entry: Metadata = Metadata(entry_json)
        evaluator = LicenseEvaluator()
        evaluator.analyze(metadata_entry)

        evaluator.reset()
        self.assertEqual(evaluator.license, '')
        self.assertFalse(evaluator.license_info_present)

    def test_result(self) -> None:
        f = open("test/data/sample.json")
        entry_json = json.load(f)
        f.close()

        metadata_entry: Metadata = Metadata(entry_json)

        evaluator = LicenseEvaluator()
        evaluator.analyze(metadata_entry)
        result = evaluator.result()

        self.assertIsNotNone(result['license'])

    def test_entry(self) -> None:
        f = open("test/data/sample.json")
        entry_json = json.load(f)
        f.close()

        metadata_entry: Metadata = Metadata(entry_json)

        evaluator = LicenseEvaluator()
        evaluator.analyze(metadata_entry)
        self.assertTrue(evaluator.license_info_present, 'License info missing')


class TestRecency(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_recency_init(self) -> None:
        evaluator = RecencyEvaluator()
        self.assertEqual(evaluator.recency, None)

    def test_reset(self) -> None:
        f = open("test/data/sample.json")
        entry_json = json.load(f)
        f.close()

        metadata_entry: Metadata = Metadata(entry_json)
        evaluator = RecencyEvaluator()
        evaluator.analyze(metadata_entry)

        evaluator.reset()
        self.assertEqual(evaluator.recency, None)

    def test_result(self) -> None:
        f = open("test/data/sample.json")
        entry_json = json.load(f)
        f.close()

        metadata_entry: Metadata = Metadata(entry_json)

        evaluator = RecencyEvaluator()
        evaluator.analyze(metadata_entry)
        result = evaluator.result()
        self.assertIsNotNone(result['recency'])

    def test_entry(self) -> None:
        f = open("test/data/sample.json")
        entry_json = json.load(f)
        f.close()

        metadata_entry: Metadata = Metadata(entry_json)

        evaluator = RecencyEvaluator()
        evaluator.analyze(metadata_entry)
        self.assertIsNotNone(evaluator.recency, 'Cannot estimate recency')
        self.assertLessEqual(evaluator.recency, 50, 'Dictionary is older than 50 years')



class TestMetadataQuantity(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_metadata_quantity_init(self) -> None:
        evaluator = MetadataQuantityEvaluator()
        self.assertEqual(evaluator.metric_count, 0)
        self.assertEqual(evaluator.total_metrics, 0)

    def test_reset(self) -> None:
        f = open("test/data/sample.json")
        entry_json = json.load(f)
        f.close()

        metadata_entry: Metadata = Metadata(entry_json)

        evaluator = MetadataQuantityEvaluator()
        evaluator.analyze(metadata_entry)
        evaluator.reset()

        self.assertEqual(evaluator.metric_count, 0)
        self.assertEqual(evaluator.total_metrics, 0)

    def test_result(self) -> None:
        f = open("test/data/sample.json")
        entry_json = json.load(f)
        f.close()

        metadata_entry: Metadata = Metadata(entry_json)

        evaluator = MetadataQuantityEvaluator()
        evaluator.analyze(metadata_entry)
        # print(str(evaluator.metric_count) +'/'+str(evaluator.total_metrics))
        # TODO - what is the expected ratio?
        result = evaluator.result()
        self.assertIsNotNone(result['metric count'])
        self.assertIsNotNone(result['total metrics'])

    def test_entry(self) -> None:
        f = open("test/data/sample.json")
        entry_json = json.load(f)
        f.close()

        metadata_entry: Metadata = Metadata(entry_json)

        evaluator = MetadataQuantityEvaluator()
        evaluator.analyze(metadata_entry)
        self.assertGreaterEqual(evaluator.metric_count, evaluator.total_metrics / 10, 'Less than 10% of metadata')


from edie.api import ApiClient
api = ApiClient(endpoint='http://lexonomy.elex.is/',api_key='GXCQJ6S2FZUATM5Z2S0MGZ7XOMXKUFNP')

class TestLexonomyAboutDict(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_lexonomy_about_dict_init(self) -> None:
        evaluator = LexonomyAboutDictEvaluator()
        self.assertEqual(evaluator.metrics, 0)
        self.assertIsNone(evaluator.source_language, 0)
        self.assertIsNone(evaluator.target_language, 0)

    def test_entry(self):
        f = open("test/data/dictionaries.json")
        entry_json = json.load(f)
        f.close()

        for dict in entry_json['dictionaries'][:10]:
            about = api.about(dictionary_id=dict)

            metadata_entry: Metadata = Metadata(about)

            evaluator = LexonomyAboutDictEvaluator()
            evaluator.analyze(metadata_entry)
            # print(evaluator.result())

            try:
                self.assertIsNotNone(evaluator.source_language,msg='missing source language '+dict)
                self.assertIsNotNone(evaluator.target_language,msg='missing target language '+dict)
                self.assertGreater(evaluator.metrics,0)

            except:
                print('assertion failed')


    def test_result(self):
        f = open("test/data/dictionaries.json")
        entry_json = json.load(f)
        f.close()

        for dict in entry_json['dictionaries'][:10]:
            about = api.about(dictionary_id=dict)

            metadata_entry: Metadata = Metadata(about)

            evaluator = LexonomyAboutDictEvaluator()
            evaluator.analyze(metadata_entry)
            result = evaluator.result()

            self.assertIsNotNone(result['source language'])
            self.assertIsNotNone(result['target language'])
            self.assertIsNotNone(result['total metric count'])

            # print(evaluator.result())

    def test_reset(self):
        f = open("test/data/dictionaries.json")
        entry_json = json.load(f)
        f.close()

        for dict in entry_json['dictionaries'][:10]:
            about = api.about(dictionary_id=dict)

            metadata_entry: Metadata = Metadata(about)

            evaluator = LexonomyAboutDictEvaluator()
            evaluator.analyze(metadata_entry)

            evaluator.reset()

            self.assertEqual(evaluator.metrics, 0)
            self.assertIsNone(evaluator.source_language, 0)
            self.assertIsNone(evaluator.target_language, 0)




class TestMetadataApiResponse(unittest.TestCase):
    '''
    designed to test the API response for all dictionaries
    using a sample json from https://lexonomy.elex.is/api/listDict
    '''
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_metadata_api_response_init(self) -> None:
        evaluator = ApiMetadataResponseEvaluator()
        self.assertEqual(len(evaluator.languages), 0)
        self.assertEqual(evaluator.dict_count, 0)

    def test_reset(self) -> None:
        f = open("test/data/lexonomy.json")
        entry_json = json.load(f)
        f.close()

        api_entry: JsonApiResponse = JsonApiResponse(entry_json)
        evaluator = ApiMetadataResponseEvaluator()

        evaluator.analyze(api_entry)

        evaluator.reset()

        self.assertEqual(len(evaluator.languages), 0)
        self.assertEqual(evaluator.dict_count, 0)

    def test_result(self) -> None:
        f = open("test/data/lexonomy.json")
        entry_json = json.load(f)
        f.close()

        api_entry: JsonApiResponse = JsonApiResponse(entry_json)
        evaluator = ApiMetadataResponseEvaluator()

        evaluator.analyze(api_entry)
        result = evaluator.result()

        self.assertIsNotNone(result['dictionary count'])

    def test_entry(self) -> None:
        f = open("test/data/lexonomy.json")
        entry_json = json.load(f)
        f.close()

        api_entry: JsonApiResponse = JsonApiResponse(entry_json)
        evaluator = ApiMetadataResponseEvaluator()

        evaluator.analyze(api_entry)

        self.assertGreaterEqual(evaluator.dict_count, 1)



if __name__ == '__main__':
    unittest.main()
