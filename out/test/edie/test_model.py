import sys
import unittest
import json

from edie.model import *


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
