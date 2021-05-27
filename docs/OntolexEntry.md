# OntolexEntry


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**context** | **str** | The JSON-LD Context Document, which should be derived from the OntoLex JSON spec | 
**id** | **str** | The identifier of this resource | 
**type** | **str** | The type of this entry | 
**canonical_form** | [**OntolexEntryCanonicalForm**](OntolexEntryCanonicalForm.md) |  | 
**senses** | [**[OntolexLexicalSense]**](OntolexLexicalSense.md) | The sense property relates a lexical entry to one of its lexical senses. | 
**part_of_speech** | **str** | The part of speech of the entry | [optional] 
**other_form** | [**[OntolexForm]**](OntolexForm.md) | The other form property relates a lexical entry to a non-preferred (\&quot;non-lemma\&quot;) form that realizes the given lexical entry. | [optional] 
**morphological_pattern** | **str** | The morphological pattern property indicates the morphological class of a word. | [optional] 
**etymology** | **str** | The etymology of the entry | [optional] 
**usage** | **str** | The usage property indicates usage conditions or pragmatic implications when using the lexical entry to refer to the given ontological meaning. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


