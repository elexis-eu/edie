import unittest
import json
from unittest import TestCase
from xml.etree.ElementTree import ParseError

from edie.model import *
from edie.helper import validate_tei


class TestParsing(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testReadAbout(self):
        data = json.loads("""{
  "release": "PUBLIC",
  "sourceLanguage": "en",
  "targetLanguage": [
    "en",
    "de"
  ],
  "genre": [
    "gen"
  ],
  "license": "https://creativecommons.org/licenses/by/4.0/",
  "title": "The Human-Readable Name of this resource",
  "creator": [
    {
      "name": "Institute of This Resource",
      "email": "contact@institute.com"
    }
  ],
  "publisher": [
    {
      "name": "Publishing Company"
    }
  ]
}""")
        result = Metadata(data)
        self.assertEqual(len(result.errors), 0)

    def testEntry(self):
        data = json.loads("""{
    "release": "PUBLIC",
    "lemma": "string",
    "language": "en",
    "id": "string",
    "partOfSpeech": [
      "ADJ"
    ],
    "formats": [
      "tei"
    ]
  }""")
        result = Entry(data)
        self.assertEqual(len(result.errors), 0)

    def testJsonEntry(self):
        data = json.loads("""{
  "@context": "http://lexinfo.net/jsonld/3.0/content.json",
  "@type": "Word",
  "language": "en",
  "partOfSpeech": "commonNoun",
  "canonicalForm": {
    "writtenRep": "example"
  },
  "senses": [
    {
      "definition": "An example OntoLex Entry"
    }
  ]
}""")
        result = JsonEntry(data)
        self.assertEqual(len(result.errors), 0)
        self.assertEqual(len(result.senses), 1)
        self.assertEqual(result.senses[0].definition, "An example OntoLex Entry")

    def testValidateNonTei(self):
        entry = "{this is not xml}"

        self.assertRaises(ParseError, validate_tei, entry)

    def testValidateTei(self):
        entry = """<entry xml:id="id">
                            <form type="lemma"><orth>example</orth></form>
                            <gramGrp>
                                <pos norm="NN">noun</pos>
                            </gramGrp>
                            <sense n="1">
                                <def>An example TEI-Lex0 Entry</def>
                            </sense>
                            <sense n="2">
                                <def>Another example</def>
                            </sense>
                        </entry>"""

        result = validate_tei(entry)

        self.assertTrue(isinstance(result, Element))

    def testTeiDocument(self):
        entry = """<entry xml:id="id">
                            <form type="lemma"><orth>example</orth></form>
                            <gramGrp>
                                <pos norm="NN">noun</pos>
                            </gramGrp>
                            <sense n="1">
                                <def>An example TEI-Lex0 Entry</def>
                            </sense>
                            <sense n="2">
                                <def>Another example</def>
                            </sense>
                        </entry>"""
        tei_entry = validate_tei(entry)

        json_entry: JsonEntry = JsonEntry.from_tei_entry(tei_entry, "test")

        self.assertTrue(isinstance(json_entry, JsonEntry))
        self.assertEqual(len(json_entry.errors), 0)
        self.assertEqual(json_entry.canonical_form.written_rep, "example")
        self.assertEqual(json_entry.part_of_speech, PartOfSpeech.COMMON_NOUN)
        self.assertEqual(len(json_entry.senses), 2)
        self.assertEqual(json_entry.senses[0].definition, "An example TEI-Lex0 Entry")
        self.assertEqual(json_entry.senses[1].definition, "Another example")


class TestMetadata(TestCase):
    def test_metadata_with_error(self):
        with open('test/data/about_with_error.json') as about_file:
            metadata = Metadata(about_file)

            self.assertGreater(len(metadata.errors), 0)
