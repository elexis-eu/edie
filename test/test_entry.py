"""
    ELEXIS Protocol for accessing dictionaries

    This protocol allows data to be shared with the ELEXIS platform and should be implemented by all providers of data to the ELEXIS platform. This is an OpenAPI documentation, for more details about using this specification, please refer to OpenAPI documentations: https://swagger.io/resources/articles/documenting-apis-with-swagger/  # noqa: E501

    The version of the OpenAPI document: 1.0
    Generated by: https://openapi-generator.tech
"""

import sys
import unittest
import json

from src.elexis_client.model import JsonEntry
from src.metrics.base import NumberOfSensesEvaluator


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


class TestNumberOfSenses(unittest.TestCase):

    def setUp(self):
        self.numberOfSensesEvaluator: NumberOfSensesEvaluator = NumberOfSensesEvaluator()

    def tearDown(self):
        pass

    def testEntry(self):
        f = open("data/entries.json")
        entry_json = json.load(f)
        entry: JsonEntry = JsonEntry(entry_json)
        evaluator = NumberOfSensesEvaluator()

        evaluator.accumulate(entry)

        self.assertEqual(evaluator.senses_count, 1)
        self.assertEqual(evaluator.entry_count, 1)


if __name__ == '__main__':
    unittest.main()
