"""
    ELEXIS Protocol for accessing dictionaries

    This protocol allows data to be shared with the ELEXIS platform and should be implemented by all providers of data to the ELEXIS platform. This is an OpenAPI documentation, for more details about using this specification, please refer to OpenAPI documentations: https://swagger.io/resources/articles/documenting-apis-with-swagger/  # noqa: E501

    The version of the OpenAPI document: 1.0
    Generated by: https://openapi-generator.tech
"""


import unittest

import openapi_client
from openapi_client.api.default_api import DefaultApi  # noqa: E501


class TestDefaultApi(unittest.TestCase):
    """DefaultApi unit test stubs"""

    def setUp(self):
        self.api = DefaultApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_about(self):
        """Test case for about

        About the dictionary  # noqa: E501
        """
        pass

    def test_dictionaries(self):
        """Test case for dictionaries

        Get dictionaries  # noqa: E501
        """
        pass

    def test_get_all(self):
        """Test case for get_all

        Get all lemmas  # noqa: E501
        """
        pass

    def test_get_by_lemma(self):
        """Test case for get_by_lemma

        Headword lookup  # noqa: E501
        """
        pass

    def test_get_entry_as_onto_lex_by_id(self):
        """Test case for get_entry_as_onto_lex_by_id

        Entry as Turtle  # noqa: E501
        """
        pass

    def test_get_entry_as_teiby_id(self):
        """Test case for get_entry_as_teiby_id

        Entry XML  # noqa: E501
        """
        pass

    def test_get_entry_by_id(self):
        """Test case for get_entry_by_id

        Entry as JSON  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
