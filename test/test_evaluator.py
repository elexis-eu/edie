import json
from unittest import TestCase
from unittest.mock import patch, Mock

from edie.evaluator import Edie
from edie.model import Dictionary


class TestEdie(TestCase):
    def test_init_edie(self):
        pass

    @patch('edie.api.ApiClient')
    def test_load_specific_dictionaries(self, api_client):
        with open('test/data/about.json') as about_file:
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
        with open('test/data/dictionaries.json') as dictionaries_file, open('test/data/about.json') as about_file:
            api_client.dictionaries.return_value = json.load(dictionaries_file)
            api_client.about.return_value = json.load(about_file)
            edie = Edie(api_client)

            response: [Dictionary] = edie.load_dictionaries()

            api_client.dictionaries.assert_called_once()
            self.assertEqual(api_client.about.call_count, 2)
            self.assertEqual(len(response), 2)
            self.assertEqual(len(edie.dictionaries), 2)
            self.assertIsInstance(edie.dictionaries[0], Dictionary)
