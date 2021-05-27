# Entry


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**release** | **str** | The conditions under which this entry can be included in the ELEXIS Matrix Dictionary | 
**lemma** | **str** | The lemma of this identifier | 
**id** | **str** | A unique identifier for the entry | 
**language** | **str** | A language code following the ISO 639-1,2,3 standard. If a (two-letter) ISO 639-1 code exists this should be used in preference | [optional] 
**part_of_speech** | **[str]** | A part of speech tag that the entry has, this must be one of the value from the Universal Part-of-Speech Tagset (http://universaldependencies.org/u/pos/) | [optional] 
**formats** | **[str]** | The formats that this resource is available in. They are as follows  - &#x60;tei&#x60;: This document is available as TEI-Lex0 from the &#x60;/tei&#x60; path  - &#x60;json&#x60;: This document is available as OntoLex-Lemon in JSON-LD markup from the &#x60;/json&#x60; path  - &#x60;ontolex&#x60;: The document is available as OntoLex-Lemon in Turtle from the &#x60;/ontolex&#x60; path | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


