from xml.etree import ElementTree
from edie.model import JsonEntry


def convert_tei(tei_entry, errors=[], entry_id="NO_ID"):
    """Convert a TEI entry into Json
    tei_entry: The entry as a string
    errors: Pass an array to collect errors
    entry_id: An identifier for the error"""
    try:
        doc = ElementTree.fromstring(tei_entry)
        entries = []
        for entry_elem in doc.iter("entry"):
            entry = {}
            for form_elem in doc.iter("form"):
                if form_elem.attrib["type"] == "lemma":
                    for orth_elem in doc.iter("orth"):
                        if "canonicalForm" in entry:
                            errors.append("Multiple lemmas for entry %s" % entry_id)
                        else:
                            entry["canonicalForm"] = {
                                "writtenRep": orth_elem.text
                            }

            for gramgrp_elem in doc.iter("gramGrp"):
                for pos in gramgrp_elem.iter("pos"):
                    if "norm" in pos.attrib:
                        entry["partOfSpeech"] = normalise_pos(pos.attrib["norm"], errors)
                    else:
                        entry["partOfSpeech"] = normalise_pos(pos.text, errors)

            entry["senses"] = []
            for sense in doc.iter("sense"):
                sense_dict = {}
                for defn in sense.iter("def"):
                    sense_dict["definition"] = defn.text
                entry["senses"].append(sense_dict)

            entries.append(JsonEntry(entry))
        return entries
    except Exception as e:
        errors.append("Error with entry %s: %s" % (entry_id, str(e)))


def normalise_pos(pos, errors):
    if pos in ["adjective", "adposition", "adverb", "auxiliary",
               "coordinatingConjunction", "determiner", "interjection",
               "commonNoun", "numeral", "particle", "pronoun", "properNoun",
               "punctuation", "subordinatingConjunction", "symbol", "verb",
               "other"]:
        return pos
    elif pos == "ADJ":
        return "adjective"
    elif pos == "ADP":
        return "adposition"
    elif pos == "ADV":
        return "adverb"
    elif pos == "AUX":
        return "auxiliary"
    elif pos == "CCONJ":
        return "coordinatingConjunction"
    elif pos == "DET":
        return "determiner"
    elif pos == "INTJ":
        return "interjection"
    elif pos == "NN":
        return "commonNoun"
    elif pos == "NOUN":
        return "commonNoun"
    elif pos == "NUM":
        return "numeral"
    elif pos == "PART":
        return "particle"
    elif pos == "PRON":
        return "pronoun"
    elif pos == "PROPN":
        return "properNoun"
    elif pos == "PUNCT":
        return "punctuation"
    elif pos == "SCONJ":
        return "subordinatingConjunction"
    elif pos == "SYM":
        return "symbol"
    elif pos == "VB":
        return "verb"
    elif pos == "VERB":
        return "verb"
    elif pos == "X":
        return "other"
    else:
        errors.append("Unsupported part-of-speech value: %s" % pos)
        return "other"
