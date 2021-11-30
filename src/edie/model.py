import re
import dateutil.parser
from enum import Enum


class Metadata(object):
    def __init__(self, json):  # noqa: E501
        """ The metadata object
            abstract (str): A summary of the resource.. [optional]  # noqa: E501
            accrual_method (str): The method by which items are added to a collection.. [optional]  # noqa: E501
            accrual_periodicity (str): The frequency with which items are added to a collection.. [optional]  # noqa: E501
            accrual_policy (str): The policy governing the addition of items to a collection.. [optional]  # noqa: E501
            alternative (str): An alternative name for the resource.. [optional]  # noqa: E501
            audience (str): A class of entity for whom the resource is intended or useful.. [optional]  # noqa: E501
            available (date): Date that the resource became or will become available.. [optional]  # noqa: E501
            bibliographic_citation (str): A bibliographic reference for the resource.. [optional]  # noqa: E501
            conforms_to (str): An established standard to which the described resource conforms.. [optional]  # noqa: E501
            contributor ([Agent]): An entity responsible for making contributions to the resource.. [optional]  # noqa: E501
            coverage (str): The spatial or temporal topic of the resource, the spatial applicability of the resource, or the jurisdiction under which the resource is relevant.. [optional]  # noqa: E501
            created (date): Date of creation of the resource.. [optional]  # noqa: E501
            date (DateTime): A point or period of time associated with an event in the lifecycle of the resource.. [optional]  # noqa: E501
            date_accepted (date): Date of acceptance of the resource.. [optional]  # noqa: E501
            date_copyrighted (date): Date of copyright.. [optional]  # noqa: E501
            date_submitted (date): Date of submission of the resource.. [optional]  # noqa: E501
            description (str): An account of the resource.. [optional]  # noqa: E501
            education_level (str): A class of entity, defined in terms of progression through an educational or training context, for which the described resource is intended.. [optional]  # noqa: E501
            extent (str): The size or duration of the resource.. [optional]  # noqa: E501
            has_format (str): A related resource that is substantially the same as the pre-existing described resource, but in another format.. [optional]  # noqa: E501
            has_part (str): A related resource that is included either physically or logically in the described resource.. [optional]  # noqa: E501
            has_version (str): A related resource that is a version, edition, or adaptation of the described resource.. [optional]  # noqa: E501
            identifier (str): An unambiguous reference to the resource within a given context.. [optional]  # noqa: E501
            instructional_method (str): A process, used to engender knowledge, attitudes and skills, that the described resource is designed to support.. [optional]  # noqa: E501
            is_format_of (str): A related resource that is substantially the same as the described resource, but in another format.. [optional]  # noqa: E501
            is_part_of (str): A related resource in which the described resource is physically or logically included.. [optional]  # noqa: E501
            is_referenced_by (str): A related resource that references, cites, or otherwise points to the described resource.. [optional]  # noqa: E501
            is_replaced_by (str): A related resource that supplants, displaces, or supersedes the described resource.. [optional]  # noqa: E501
            is_required_by (str): A related resource that requires the described resource to support its function, delivery, or coherence.. [optional]  # noqa: E501
            issued (date): Date of formal issuance (e.g., publication) of the resource.. [optional]  # noqa: E501
            is_version_of (str): A related resource of which the described resource is a version, edition, or adaptation.. [optional]  # noqa: E501
            mediator ([AgentClass]): An entity that mediates access to the resource and for whom the resource is intended or useful.. [optional]  # noqa: E501
            modified (date): Date on which the resource was changed.. [optional]  # noqa: E501
            provenance (str): A statement of any changes in ownership and custody of the resource since its creation that are significant for its authenticity, integrity, and interpretation.. [optional]  # noqa: E501
            references (str): A related resource that is referenced, cited, or otherwise pointed to by the described resource.. [optional]  # noqa: E501
            relation (str): A related resource.. [optional]  # noqa: E501
            replaces (str): A related resource that is supplanted, displaced, or superseded by the described resource.. [optional]  # noqa: E501
            requires (str): A related resource that is required by the described resource to support its function, delivery, or coherence.. [optional]  # noqa: E501
            rights (str): Information about rights held in and over the resource.. [optional]  # noqa: E501
            rights_holder ([Agent]): A person or organization owning or managing rights over the resource.. [optional]  # noqa: E501
            source (str): A related resource from which the described resource is derived.. [optional]  # noqa: E501
            spatial (str): Spatial characteristics of the resource.. [optional]  # noqa: E501
            subject (str): The topic of the resource.. [optional]  # noqa: E501
            table_of_contents (str): A list of subunits of the resource.. [optional]  # noqa: E501
            temporal (str): Temporal characteristics of the resource.. [optional]  # noqa: E501
            type (str): The nature or genre of the resource.. [optional]  # noqa: E501
            valid (date): Date of validity of a resource.. [optional]  # noqa: E501
        """
        self.errors = []

        if "release" in json:
            if json["release"] in ["PUBLIC", "NONCOMMERCIAL", "RESEARCH", "PRIVATE"]:
                self.release = json["release"]
            else:
                self.errors.append("Release value was invalid: "
                                   + str(json["release"]))
                self.release = None
        else:
            self.errors.append("Release not specified")
            self.release = None

        if "sourceLanguage" in json:
            if (isinstance(json["sourceLanguage"], str) and
                    re.match("^\\w{2,3}$", json["sourceLanguage"])):
                self.source_language = json["sourceLanguage"]
            else:
                self.errors.append("Source language value was invalid: "
                                   + str(json["sourceLanguage"]))
                self.source_language = None
        else:
            self.errors.append("Source language not specified")
            self.source_language = None

        if "targetLanguage" in json:
            if (isinstance(json["targetLanguage"], list) and
                    all(isinstance(x, str) and re.match("^\\w{2,3}$", x)
                        for x in json["targetLanguage"])):
                self.target_language = json["targetLanguage"]
            else:
                self.errors.append("Target language value was invalid: "
                                   + str(json["targetLanguage"]))
                self.target_language = None
        else:
            self.errors.append("Target language(s) not specified")
            self.target_language = None

        if "genre" in json:
            if (isinstance(json["genre"], list) and
                    all(g in ["gen", "lrn", "ety", "spe", "his", "ort", "trm"]
                        for g in json["genre"])):
                self.genre = json["genre"]
            else:
                self.errors.append("Genre value was invalid: "
                                   + str(json["genre"]))
                self.genre = None
        else:
            self.errors.append("Genre(s) not specified")

        if "license" in json:
            if (isinstance(json["license"], str) and
                    re.match("^https?:.*$", json["license"])):
                self.license = json["license"]
            else:
                self.errors.append("License value was invalid: "
                                   + str(json["license"]))
                self.license = None
        else:
            self.errors.append("License not specified")
            self.license = None

        if "title" in json:
            if isinstance(json["title"], str):
                self.title = json["title"]
            else:
                self.errors.append("Title value was invalid: "
                                   + str(json["title"]))
                self.title = None
        else:
            self.errors.append("Title not specified")
            self.title = None

        if "creator" in json:
            if (isinstance(json["creator"], list) and
                    all(isinstance(a, object) for a in json["creator"])):
                self.agent = [Agent(a) for a in json["creator"]]
                for a in self.agent:
                    self.errors.extend(a.errors)
            else:
                self.errors.append("Creator value was invalid: "
                                   + str(json["creator"]))
                self.agent = None
        else:
            self.errors.append("Creator not specified")
            self.title = None

        if "publisher" in json:
            # self.agent instead of self.publisher ?
            if (isinstance(json["publisher"], list) and
                    all(isinstance(a, object) for a in json["publisher"])):
                self.agent = [Agent(a) for a in json["publisher"]]
                for a in self.agent:
                    self.errors.extend(a.errors)
            else:
                self.errors.append("Publisher value was invalid: "
                                   + str(json["publisher"]))
                self.agent = None
        else:
            self.errors.append("Publisher not specified")
            self.title = None
        self.abstract = self._extract_string_prop(json, 'abstract')
        self.accrual_method = self._extract_string_prop(json, 'accrualMethod')
        self.accrual_periodicity = self._extract_string_prop(json, 'accrualPeriodicity')
        self.accrual_policy = self._extract_string_prop(json, 'accrualPolicy')
        self.alternative = self._extract_string_prop(json, 'alternative')
        self.audience = self._extract_string_prop(json, 'audience')
        self.available = self._extract_date_prop(json, 'available')
        self.bibliographic_citation = self._extract_string_prop(json, 'bibliographicCitation')
        self.conforms_to = self._extract_string_prop(json, 'conformsTo')
        self.contributor = self._extract_agent_prop(json, 'contributor')
        self.coverage = self._extract_string_prop(json, 'coverage')
        self.created = self._extract_date_prop(json, 'created')
        self.date = self._extract_date_prop(json, 'date')
        self.date_accepted = self._extract_date_prop(json, 'dateAccepted')
        self.date_copyrighted = self._extract_date_prop(json, 'dateCopyrighted')
        self.date_submitted = self._extract_date_prop(json, 'dateSubmitted')
        self.description = self._extract_string_prop(json, 'description')
        self.education_level = self._extract_string_prop(json, 'educationLevel')
        self.extent = self._extract_string_prop(json, 'extent')
        self.has_format = self._extract_string_prop(json, 'hasFormat')
        self.has_part = self._extract_string_prop(json, 'hasPart')
        self.has_version = self._extract_string_prop(json, 'hasVersion')
        self.identifier = self._extract_string_prop(json, 'identifier')
        self.instructional_method = self._extract_string_prop(json, 'instructionalMethod')
        self.is_format_of = self._extract_string_prop(json, 'isFormatOf')
        self.is_part_of = self._extract_string_prop(json, 'isPartOf')
        self.is_referenced_by = self._extract_string_prop(json, 'isReferencedBy')
        self.is_replaced_by = self._extract_string_prop(json, 'isReplacedBy')
        self.is_required_by = self._extract_string_prop(json, 'isRequiredBy')
        self.issued = self._extract_date_prop(json, 'issued')
        self.is_version_of = self._extract_string_prop(json, 'isVersionOf')
        self.mediator = self._extract_agent_prop(json, 'mediator')
        self.modified = self._extract_date_prop(json, 'modified')
        self.provenance = self._extract_string_prop(json, 'provenance')
        self.references = self._extract_string_prop(json, 'references')
        self.relation = self._extract_string_prop(json, 'relation')
        self.replaces = self._extract_string_prop(json, 'replaces')
        self.requires = self._extract_string_prop(json, 'requires')
        self.rights = self._extract_string_prop(json, 'rights')
        self.rights_holder = self._extract_agent_prop(json, 'rightsHolder')
        self.source = self._extract_string_prop(json, 'source')
        self.spatial = self._extract_string_prop(json, 'spatial')
        self.subject = self._extract_string_prop(json, 'subject')
        self.table_of_contents = self._extract_string_prop(json, 'tableOfContents')
        self.temporal = self._extract_string_prop(json, 'temporal')
        self.type = self._extract_string_prop(json, 'type')
        self.valid = self._extract_date_prop(json, 'valid')

    def _extract_string_prop(self, json, prop):
        if prop in json:
            if isinstance(json[prop], str):
                return json[prop]
            else:
                self.errors.append(f"Value for {prop} was invalid: {json[prop]}")
        return None

    def _extract_date_prop(self, json, prop):
        if prop in json:
            if isinstance(json[prop], str):
                try:
                    return dateutil.parser.parse(json[prop])
                except:
                    self.errors.append(f"Value for {prop} was invalid: {json[prop]}")
            else:
                self.errors.append(f"Value for {prop} was invalid: {json[prop]}")
        return None

    def _extract_agent_prop(self, json, prop):
        if prop in json:
            if (isinstance(json[prop], list) and
                    all(isinstance(a, object) for a in json[prop])):
                return [Agent(a) for a in json[prop]]
                for a in self.agent:
                    self.errors.extend(a.errors)
            else:
                self.errors.append(f"Value for {prop} was invalid: {json[prop]}")
        return None


class Agent(object):
    def __init__(self, json):
        self.errors = []
        if "name" in json:
            self.name = json["name"]
        else:
            self.name = None
        if "email" in json:
            self.email = json["email"]
        else:
            self.email = None
        if "url" in json:
            self.url = json["url"]
        else:
            self.url = None


class Entry(object):
    def __init__(self, json):
        self.errors = []
        if "release" in json:
            if json["release"] in ["PUBLIC", "NONCOMMERCIAL", "RESEARCH", "PRIVATE"]:
                self.release = json["release"]
            else:
                self.errors.append("Release value was invalid: "
                                   + str(json["release"]))
                self.release = None
        else:
            self.errors.append("Release not specified")
            self.release = None

        if "lemma" in json:
            if isinstance(json["lemma"], str):
                self.lemma = json["lemma"]
            else:
                self.errors.append("Lemma value was invalid: "
                                   + str(json["lemma"]))
                self.lemma = None
        else:
            self.errors.append("Lemma not specified")
            self.lemma = None

        if "language" in json:
            if (isinstance(json["language"], str) and
                    re.match("^\\w{2,3}$", json["language"])):
                self.language = json["language"]
            else:
                self.errors.append("Language value was invalid: "
                                   + str(json["language"]))
                self.language = None
        else:
            self.language = None

        if "id" in json:
            if isinstance(json["id"], str):
                self.id = json["id"]
            else:
                self.errors.append("ID value was invalid: "
                                   + str(json["id"]))
                self.id = None
        else:
            self.errors.append("ID not specified")
            self.id = None

        if "partOfSpeech" in json:
            if (isinstance(json["partOfSpeech"], list) and
                    all(p in ["ADJ", "ADP", "ADV", "AUX", "CCONJ",
                              "DET", "INTJ", "NOUN", "NUM", "PART", "PRON", "PROPN",
                              "PUNCT", "SCONJ", "SYM", "VERB", "X"]
                        for p in json["partOfSpeech"])):
                self.part_of_speech = [parse_part_of_speech(p, self.errors)
                        for p in json["partOfSpeech"]]
            else:
                self.errors.append("Part of speech value was invalid: "
                                   + str(json["partOfSpeech"]))
                self.part_of_speech = None
        else:
            self.part_of_speech = None

        if "formats" in json:
            if (isinstance(json["formats"], list) and
                    all(f in ["tei", "json", "ontolex"] for f in json["formats"])):
                self.formats = json["formats"]
            else:
                self.errors.append("Format value was invalid: "
                                   + str(json["formats"]))
                self.formats = []
        else:
            self.formats = []


class JsonEntry(object):
    def __init__(self, json):
        self.errors = []
        if "@type" in json:
            if json["@type"] in ["LexicalEntry", "Word",
                    "MultiWordExpression", "Affix"]:
                self.type = json["@type"]
            else:
                self.errors.append("Invalid entry type: " +
                        str(json["@type"]))
                self.type = None
        else:
            self.errors.append("No type of entry")
            self.type = None

        if "canonicalForm" in json:
            if isinstance(json["canonicalForm"], dict):
                self.canonical_form = JsonForm(json["canonicalForm"])
                self.errors.extend(self.canonical_form.errors)
            else:
                self.errors.append("Canonical form was not an object but" +
                        str(json["canonicalForm"]))
                self.canonical_form = None
        else:
            self.errors.append("No canonical form")
            self.canonical_form = None

        if "partOfSpeech" in json:
            if json["partOfSpeech"] in ["adjective", "adposition", "adverb",
                    "auxiliary", "coordinatingConjunction", "determiner",
                    "interjection", "commonNoun", "numeral", "particle", "pronoun",
                    "properNoun", "punctuation", "subordinatingConjunction",
                    "symbol", "verb", "other"]:
                self.part_of_speech = parse_part_of_speech(json["partOfSpeech"],
                        self.errors)
            else:
                self.errors.append("Bad part of speech value: " +
                        str(json["partOfSpeech"]))
                self.part_of_speech = None
        else:
            self.part_of_speech = None

        if "otherForm" in json:
            if (isinstance(json["otherForm"], list) and
                    all(isinstance(form, dict) for form in json["otherForm"])):
                self.other_form = [JsonForm(form) for form in
                        json["otherForm"]]
                for form in self.other_form:
                    self.errors.extend(form.errors)
            else:
                self.errors.append("Bad value for other form: " +
                        str(json["otherForm"]))
                self.other_form = []
        else:
            self.other_form = []

        if "morphologicalPattern" in json:
            if isinstance(json["morphologicalPattern"], str):
                self.morphological_pattern = json["morphologicalPattern"]
            else:
                self.errors.append("Bad morphological pattern: " +
                        str(json["morphologicalPattern"]))
                self.morphological_pattern = None
        else:
            self.morphological_pattern = None

        if "etymology" in json:
            if isinstance(json["etymology"], str):
                self.etymology = json["etymology"]
            else:
                self.errors.append("Bad etymology: " +
                        str(json["etymology"]))
                self.etymology = None
        else:
            self.etymology = None

        if "senses" in json:
            if (isinstance(json["senses"], list) and
                    all(isinstance(sense, dict) for sense in json["senses"])):
                self.senses = [JsonSense(sense) for sense in json["senses"]]
            else:
                self.errors.append("Bad senses: " +
                        str(json["senses"]))
                self.senses = []
        else:
            self.errors.append("Entry has no senses")
            self.senses = []

        if "usage" in json:
            if isinstance(json["usage"], str):
                self.usage = json["usage"]
            else:
                self.errors.append("Bad usage: " +
                        str(json["usage"]))
                self.usage = None
        else:
            self.usage = None


class JsonForm(object):
    def __init__(self, json):
        self.errors = []
        if "writtenRep" in json:
            if isinstance(json["writtenRep"], str):
                self.written_rep = json["writtenRep"]
            else:
                self.errors.append("Bad written rep: " +
                        str(json["writtenRep"]))
                self.written_rep = None
        else:
            self.written_rep = None

        if "phoneticRep" in json:
            if isinstance(json["phoneticRep"], str):
                self.phonetic_rep = json["phoneticRep"]
            else:
                self.errors.append("Bad phonetic rep: " +
                        str(json["phoneticRep"]))
                self.phonetic_rep = None
        else:
            self.phonetic_rep = None


class JsonSense(object):
    def __init__(self, json):
        self.errors = []
        if "definition" in json:
            if isinstance(json["definition"], str):
                self.definition = json["definition"]
            else:
                self.errors.append("Bad definition: " +
                        str(json["definition"]))
                self.definition = None
        else:
            self.definition = None

        if "reference" in json:
            if isinstance(json["reference"], str):
                self.reference = json["reference"]
            else:
                self.errors.append("Bad reference: " +
                        str(json["reference"]))
                self.reference = None
        else:
            self.phonetic_rep = None


class PartOfSpeech(Enum):
    ADJECTIVE = 1
    ADPOSITION = 2
    ADVERB = 3
    AUXILIARY = 4
    COORDINATING_CONJUNCTION = 5
    DETERMINER = 6
    INTERJECTION = 7
    COMMON_NOUN = 8
    NUMERAL = 9
    PARTICLE = 10
    PRONOUN = 11
    PROPER_NOUN = 12
    PUNCTUATION = 13
    SUBORDINATING_CONJUNCTION = 14
    SYMBOL = 15
    VERB = 16
    OTHER = 17

def parse_part_of_speech(val, errors = None):
    if val == "ADJ":
        return PartOfSpeech.ADJECTIVE
    elif  val == "ADP":
        return PartOfSpeech.ADPOSITION
    elif val == "ADV":
        return PartOfSpeech.ADVERB
    elif val == "AUX":
        return PartOfSpeech.AUXILIARY
    elif val == "CCONJ":
        return PartOfSpeech.COORDINATING_CONJUNCTION
    elif val == "DET":
        return PartOfSpeech.DETERMINER
    elif val == "INTJ":
        return PartOfSpeech.INTERJECTION
    elif val == "NOUN":
        return PartOfSpeech.COMMON_NOUN
    elif val == "NUM":
        return PartOfSpeech.NUMERAL
    elif val == "PART":
        return PartOfSpeech.PARTICLE
    elif val == "PRON":
        return PartOfSpeech.PRONOUN
    elif val == "PROPN":
        return PartOfSpeech.PROPER_NOUN
    elif val == "PUNCT":
        return PartOfSpeech.PUNCTUATION
    elif val == "SCONJ":
        return PartOfSpeech.SUBORDINATING_CONJUNCTION
    elif val == "SYM":
        return PartOfSpeech.SYMBOL
    elif val == "VERB":
        return PartOfSpeech.VERB
    elif val == "X":
        return PartOfSpeech.OTHER
    elif val == "adjective":
        return PartOfSpeech.ADJECTIVE
    elif val == "adposition":
        return PartOfSpeech.ADPOSITION
    elif val == "adverb":
        return PartOfSpeech.ADVERB
    elif val == "auxiliary":
        return PartOfSpeech.AUXILIARY
    elif val == "coordinatingConjunction":
        return PartOfSpeech.COORDINATING_CONJUNCTION
    elif val == "determiner":
        return PartOfSpeech.DETERMINER
    elif val == "interjection":
        return PartOfSpeech.INTERJECTION
    elif val == "commonNoun":
        return PartOfSpeech.COMMON_NOUN
    elif val == "numeral":
        return PartOfSpeech.NUMERAL
    elif val == "particle":
        return PartOfSpeech.PARTICLE
    elif val == "pronoun":
        return PartOfSpeech.PRONOUN
    elif val == "properNoun":
        return PartOfSpeech.PROPER_NOUN
    elif val == "punctuation":
        return PartOfSpeech.PUNCTUATION
    elif val == "subordinatingConjunction":
        return PartOfSpeech.SUBORDINATING_CONJUNCTION
    elif val == "symbol":
        return PartOfSpeech.SYMBOL
    elif val == "verb":
        return PartOfSpeech.VERB
    elif val == "other":
        return PartOfSpeech.OTHER
    else:
        if errors:
            errors.append("Invalid part of speech value: " + str(val))
        return None

