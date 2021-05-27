# Metadata


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**release** | **str** | The conditions under which this dictionary (or data from this dictionary) can be included in the ELEXIS Matrix Dictionary | 
**source_language** | **str** | The language of the lemmas in the dictionary, as an ISO 639-1,2,3 code. If a (two-letter) ISO 639-1 code exists this should be used in preference | 
**target_language** | **[str]** | The languages of the entries in the dictionary, can be identical to the source language or another language (for example in a bilingual dictionary). | 
**genre** | **[str]** | The genre of the dictionary.  &#x60;gen&#x60; **General dictionaries** are dictionaries that document contemporary vocabulary and are intended for everyday reference by native and fluent speakers.    &#x60;lrn&#x60; **Learners&#39; dictionaries** are intended for people who are learning the language as a second language.   &#x60;ety&#x60; **Etymological dictionaries** are dictionaries that explain the origins of words.   &#x60;spe&#x60; **Dictionaries on special topics** are dictionaries that focus on a specific subset of the vocabulary (such as new words or phrasal verbs) or which focus on a specific dialect or variant of the language.   &#x60;his&#x60; **Historical dictionaries** are dictionaries that document previous historical states of the language.   &#x60;ort&#x60; **Spelling dictionaries** are dictionaries which codify the correct spelling and other aspects of the orthography of words.    &#x60;trm&#x60; **Terminological dictionaries** describe the vocabulary of specialized domains such as biology, mathematics or economics.    | 
**license** | **bool, date, datetime, dict, float, int, list, str, none_type** | The license that can be used to republish this data | 
**title** | **str** | The title of the resource | 
**creator** | [**[Agent]**](Agent.md) | The creator of the resource | 
**publisher** | [**[Agent]**](Agent.md) | The publisher of This Resource | 
**abstract** | **str** | A summary of the resource. | [optional] 
**accrual_method** | **str** | The method by which items are added to a collection. | [optional] 
**accrual_periodicity** | **str** | The frequency with which items are added to a collection. | [optional] 
**accrual_policy** | **str** | The policy governing the addition of items to a collection. | [optional] 
**alternative** | **str** | An alternative name for the resource. | [optional] 
**audience** | **str** | A class of entity for whom the resource is intended or useful. | [optional] 
**available** | **date** | Date that the resource became or will become available. | [optional] 
**bibliographic_citation** | **str** | A bibliographic reference for the resource. | [optional] 
**conforms_to** | **str** | An established standard to which the described resource conforms. | [optional] 
**contributor** | [**[Agent]**](Agent.md) | An entity responsible for making contributions to the resource. | [optional] 
**coverage** | **str** | The spatial or temporal topic of the resource, the spatial applicability of the resource, or the jurisdiction under which the resource is relevant. | [optional] 
**created** | **date** | Date of creation of the resource. | [optional] 
**date** | [**DateTime**](DateTime.md) | A point or period of time associated with an event in the lifecycle of the resource. | [optional] 
**date_accepted** | **date** | Date of acceptance of the resource. | [optional] 
**date_copyrighted** | **date** | Date of copyright. | [optional] 
**date_submitted** | **date** | Date of submission of the resource. | [optional] 
**description** | **str** | An account of the resource. | [optional] 
**education_level** | **str** | A class of entity, defined in terms of progression through an educational or training context, for which the described resource is intended. | [optional] 
**extent** | **str** | The size or duration of the resource. | [optional] 
**has_format** | **str** | A related resource that is substantially the same as the pre-existing described resource, but in another format. | [optional] 
**has_part** | **str** | A related resource that is included either physically or logically in the described resource. | [optional] 
**has_version** | **str** | A related resource that is a version, edition, or adaptation of the described resource. | [optional] 
**identifier** | **str** | An unambiguous reference to the resource within a given context. | [optional] 
**instructional_method** | **str** | A process, used to engender knowledge, attitudes and skills, that the described resource is designed to support. | [optional] 
**is_format_of** | **str** | A related resource that is substantially the same as the described resource, but in another format. | [optional] 
**is_part_of** | **str** | A related resource in which the described resource is physically or logically included. | [optional] 
**is_referenced_by** | **str** | A related resource that references, cites, or otherwise points to the described resource. | [optional] 
**is_replaced_by** | **str** | A related resource that supplants, displaces, or supersedes the described resource. | [optional] 
**is_required_by** | **str** | A related resource that requires the described resource to support its function, delivery, or coherence. | [optional] 
**issued** | **date** | Date of formal issuance (e.g., publication) of the resource. | [optional] 
**is_version_of** | **str** | A related resource of which the described resource is a version, edition, or adaptation. | [optional] 
**mediator** | [**[AgentClass]**](AgentClass.md) | An entity that mediates access to the resource and for whom the resource is intended or useful. | [optional] 
**modified** | **date** | Date on which the resource was changed. | [optional] 
**provenance** | **str** | A statement of any changes in ownership and custody of the resource since its creation that are significant for its authenticity, integrity, and interpretation. | [optional] 
**references** | **str** | A related resource that is referenced, cited, or otherwise pointed to by the described resource. | [optional] 
**relation** | **str** | A related resource. | [optional] 
**replaces** | **str** | A related resource that is supplanted, displaced, or superseded by the described resource. | [optional] 
**requires** | **str** | A related resource that is required by the described resource to support its function, delivery, or coherence. | [optional] 
**rights** | **str** | Information about rights held in and over the resource. | [optional] 
**rights_holder** | [**[Agent]**](Agent.md) | A person or organization owning or managing rights over the resource. | [optional] 
**source** | **str** | A related resource from which the described resource is derived. | [optional] 
**spatial** | **str** | Spatial characteristics of the resource. | [optional] 
**subject** | **str** | The topic of the resource. | [optional] 
**table_of_contents** | **str** | A list of subunits of the resource. | [optional] 
**temporal** | **str** | Temporal characteristics of the resource. | [optional] 
**type** | **str** | The nature or genre of the resource. | [optional] 
**valid** | **date** | Date of validity of a resource. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


