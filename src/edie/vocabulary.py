class Vocabulary:
    class EvaluationStatus:
        IN_PROGRESS = 'in progress'
        FAILED = 'evaluation failed'
        COMPLETED = 'evaluation completed'

    SIZE_OF_DICTIONARY = "sizeOfDictionary"
    AVG_DICTIONARY_SIZE = 'avgDictionarySize'

    ONTOLEX_COVERAGE = 'ontolexCoverage'
    TEI_COVERAGE = 'teiCoverage'
    JSON_COVERAGE = 'jsonCoverage'
    ONTOLEX_SUPPORTED_ENTRIES = 'ontolexSupportedEntries'
    TEI_SUPPORTED_ENTRIES = 'teiSupportedEntries'
    JSON_SUPPORTED_ENTRIES = 'jsonSupportedEntries'
    FORMATS_PER_ENTRY = 'formatsPerEntry'

    ENTRY_REPORT = 'entry_report'




    # REPORTING PROPERTIES
    AGGREGATION_METRICS = 'aggregationMetrics'
    DICTIONARY_SIZE = 'dictionarySize'
    FORMS_PER_ENTRY = 'formsPerEntry'
    DEFINITION_LENGTH_PER_ENTRY_BY_CHARACTER = 'definitionLengthPerEntryByCharacter'
    DEFINITION_LENGTH_PER_ENTRY_BY_TOKEN = 'definitionLengthPerEntryByToken'
    DEFINITION_LENGTH_PER_SENSE_BY_CHARACTER = 'definitionLengthPerSenseByCharacter'
    DEFINITION_LENGTH_PER_SENSE_BY_TOKEN= 'definitionLengthPerSenseByToken'
    SENSES_PER_ENTRY = 'sensesPerEntry'
    DEFINITIONS_PER_SENSE = 'definitionsPerSense'
    DEFINITIONS_PER_ENTRY = 'definitionsPerEntry'
    PUBLISHER = 'publisher'
    LICENSE = 'license'
    METADATA_FIELDS = 'metadataFields'
    METADATA_NONEMPTY_FIELDS = 'metadataNonemptyFields'
    RECENCY = 'recency'

    #ENTRY FORMATS
    ONTOLEX_FORMAT = 'ontolex'
    TEI_FORMAT = 'tei'
    JSON_FORMAT = 'json'
