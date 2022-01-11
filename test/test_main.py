import unittest
from edie.model import PartOfSpeech
from edie.tei import convert_tei

class TestMain(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testConvertNonXml(self):
        entry = "{this is not xml}"
        errors = []
        convert_tei(entry, errors, "test")
        self.assertGreater(len(errors), 0)

    def testTeiDocument(self):
        entry = """<entry xml:id="id">
  <form type="lemma"><orth>example</orth></form>
  <gramGrp>
    <pos norm="NN">noun</pos>
  </gramGrp>
  <sense n="1">
    <def>An example TEI-Lex0 Entry</def>
  </sense>
</entry>"""
        errors = []
        entries = convert_tei(entry, errors, "test")
        print(errors)
        self.assertEqual(len(errors), 0)
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].canonical_form.written_rep, "example")
        self.assertEqual(entries[0].part_of_speech, PartOfSpeech.COMMON_NOUN)
        self.assertEqual(len(entries[0].senses), 1)
        self.assertEqual(entries[0].senses[0].definition, "An example TEI-Lex0 Entry")
