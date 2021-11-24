import re
import dateutil.parser


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
                self.publisher = [Agent(a) for a in json["publisher"]]
                for a in self.agent:
                    self.errors.extend(a.errors)
            else:
                self.errors.append("Publisher value was invalid: "
                                   + str(json["publisher"]))
                self.publisher = None
        else:
            self.errors.append("Publisher not specified")
            self.publisher = None



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
    def __init__(self, obj):
        self.errors = []
        # TODO


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
                self.part_of_speech = json["partOfSpeech"]
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
        self.other_form = []
        if 'senses' in json:
            self.senses = json['senses']
        else:
            self.senses = []

        # TODO

