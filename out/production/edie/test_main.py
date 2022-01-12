from unittest import TestCase
from unittest.mock import patch, Mock

from main import Edie, Dictionary



class TestEdie(TestCase):
    def test_init_edie(self):
        pass

    def test_load_specific_dictionaries(self):
        dictionary_id = ['DICT_ID_1']
        edie = Edie()

        edie.load_dictionaries(dictionary_id)

    @patch('api.ApiClient.dictionaries')
    def test_load_dictionaries(self, mock_dictionaries):
        with open('')
        mock_dictionaries.return_value = Mock()
        mock_dictionaries =
        edie = Edie()

        dictionaries: [Dictionary] = edie.load_dictionaries()

        self.assertEqual(len(dictionaries), 2)
