# openapi_client.DefaultApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**about**](DefaultApi.md#about) | **GET** /about/{dictionary} | About the dictionary
[**dictionaries**](DefaultApi.md#dictionaries) | **GET** /dictionaries | Get dictionaries
[**get_all**](DefaultApi.md#get_all) | **GET** /list/{dictionary} | Get all lemmas
[**get_by_lemma**](DefaultApi.md#get_by_lemma) | **GET** /lemma/{dictionary}/{headword} | Headword lookup
[**get_entry_as_onto_lex_by_id**](DefaultApi.md#get_entry_as_onto_lex_by_id) | **GET** /ontolex/{dictionary}/{id} | Entry as Turtle
[**get_entry_as_teiby_id**](DefaultApi.md#get_entry_as_teiby_id) | **GET** /tei/{dictionary}/{id} | Entry XML
[**get_entry_by_id**](DefaultApi.md#get_entry_by_id) | **GET** /json/{dictionary}/{id} | Entry as JSON


# **about**
> Metadata about(dictionary)

About the dictionary

Get the metadata about the dictionary, including the conditions under which it can be included in the Dictionary Matrix

### Example

```python
import time
import openapi_client
from openapi_client.api import default_api
from openapi_client.model.inline_response500 import InlineResponse500
from openapi_client.model.metadata import Metadata
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = default_api.DefaultApi(api_client)
    dictionary = "dictionary_example" # str | Identifier of the dictionary to describe
    x_api_key = "X-API-KEY_example" # str | An API key to authorize access to this endpoint if necessary (optional)

    # example passing only required values which don't have defaults set
    try:
        # About the dictionary
        api_response = api_instance.about(dictionary)
        pprint(api_response)
    except openapi_client.ApiException as e:
        print("Exception when calling DefaultApi->about: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # About the dictionary
        api_response = api_instance.about(dictionary, x_api_key=x_api_key)
        pprint(api_response)
    except openapi_client.ApiException as e:
        print("Exception when calling DefaultApi->about: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **dictionary** | **str**| Identifier of the dictionary to describe |
 **x_api_key** | **str**| An API key to authorize access to this endpoint if necessary | [optional]

### Return type

[**Metadata**](Metadata.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |
**404** | Dictionary not found (identifier not known) |  -  |
**403** | Forbidden (API key not specified or not valid) |  -  |
**500** | Internal Server Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **dictionaries**
> InlineResponse200 dictionaries()

Get dictionaries

List all of the dictionaries that are available at this endpoint

### Example

```python
import time
import openapi_client
from openapi_client.api import default_api
from openapi_client.model.inline_response500 import InlineResponse500
from openapi_client.model.inline_response200 import InlineResponse200
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = default_api.DefaultApi(api_client)
    x_api_key = "X-API-KEY_example" # str | An API key to authorize access to this endpoint if necessary (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get dictionaries
        api_response = api_instance.dictionaries(x_api_key=x_api_key)
        pprint(api_response)
    except openapi_client.ApiException as e:
        print("Exception when calling DefaultApi->dictionaries: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_api_key** | **str**| An API key to authorize access to this endpoint if necessary | [optional]

### Return type

[**InlineResponse200**](InlineResponse200.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |
**403** | Forbidden (API key not specified or not valid) |  -  |
**500** | Internal Server Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_all**
> [Entry] get_all(dictionary)

Get all lemmas

Get all of the entries contained within this dictionary

### Example

```python
import time
import openapi_client
from openapi_client.api import default_api
from openapi_client.model.entry import Entry
from openapi_client.model.inline_response500 import InlineResponse500
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = default_api.DefaultApi(api_client)
    dictionary = "dictionary_example" # str | The identifier of the dictionary to list
    limit = 1 # int | The maximum number of entries to return (optional)
    offset = 0 # int | The offset (index of first entry) to return (optional) if omitted the server will use the default value of 0
    x_api_key = "X-API-KEY_example" # str | An API key to authorize access to this endpoint if necessary (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get all lemmas
        api_response = api_instance.get_all(dictionary)
        pprint(api_response)
    except openapi_client.ApiException as e:
        print("Exception when calling DefaultApi->get_all: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all lemmas
        api_response = api_instance.get_all(dictionary, limit=limit, offset=offset, x_api_key=x_api_key)
        pprint(api_response)
    except openapi_client.ApiException as e:
        print("Exception when calling DefaultApi->get_all: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **dictionary** | **str**| The identifier of the dictionary to list |
 **limit** | **int**| The maximum number of entries to return | [optional]
 **offset** | **int**| The offset (index of first entry) to return | [optional] if omitted the server will use the default value of 0
 **x_api_key** | **str**| An API key to authorize access to this endpoint if necessary | [optional]

### Return type

[**[Entry]**](Entry.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The entries matching with this lemma |  -  |
**404** | Dictionary not found (identifier not known) |  -  |
**403** | Forbidden (API key not specified or not valid) |  -  |
**500** | Internal Server Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_by_lemma**
> [Entry] get_by_lemma(dictionary, headword)

Headword lookup

Given a headword, find all the entries that are listed under this headword

### Example

```python
import time
import openapi_client
from openapi_client.api import default_api
from openapi_client.model.entry import Entry
from openapi_client.model.inline_response500 import InlineResponse500
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = default_api.DefaultApi(api_client)
    dictionary = "dictionary_example" # str | The identifier of the dictionary containing the entries
    headword = "headword_example" # str | The lemma of the headword to lookup
    part_of_speech = "ADJ" # str | A part of speech tag that the entry has, this must be one of the value from the Universal Part-of-Speech Tagset (http://universaldependencies.org/u/pos/) (optional)
    limit = 1 # int | The maximum number of entries to return (optional)
    offset = 0 # int | The offset (index of first entry) to return (optional) if omitted the server will use the default value of 0
    inflected = False # bool | If true treat the query as an inflected form and return all lemmas that may be a form of this query (optional) if omitted the server will use the default value of False
    x_api_key = "X-API-KEY_example" # str | An API key to authorize access to this endpoint if necessary (optional)

    # example passing only required values which don't have defaults set
    try:
        # Headword lookup
        api_response = api_instance.get_by_lemma(dictionary, headword)
        pprint(api_response)
    except openapi_client.ApiException as e:
        print("Exception when calling DefaultApi->get_by_lemma: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Headword lookup
        api_response = api_instance.get_by_lemma(dictionary, headword, part_of_speech=part_of_speech, limit=limit, offset=offset, inflected=inflected, x_api_key=x_api_key)
        pprint(api_response)
    except openapi_client.ApiException as e:
        print("Exception when calling DefaultApi->get_by_lemma: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **dictionary** | **str**| The identifier of the dictionary containing the entries |
 **headword** | **str**| The lemma of the headword to lookup |
 **part_of_speech** | **str**| A part of speech tag that the entry has, this must be one of the value from the Universal Part-of-Speech Tagset (http://universaldependencies.org/u/pos/) | [optional]
 **limit** | **int**| The maximum number of entries to return | [optional]
 **offset** | **int**| The offset (index of first entry) to return | [optional] if omitted the server will use the default value of 0
 **inflected** | **bool**| If true treat the query as an inflected form and return all lemmas that may be a form of this query | [optional] if omitted the server will use the default value of False
 **x_api_key** | **str**| An API key to authorize access to this endpoint if necessary | [optional]

### Return type

[**[Entry]**](Entry.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The entries matching with this query |  -  |
**403** | Forbidden (API key not specified or not valid) |  -  |
**404** | Dictionary not found (identifier not known) |  -  |
**500** | Internal Server Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_entry_as_onto_lex_by_id**
> get_entry_as_onto_lex_by_id(dictionary, id)

Entry as Turtle

Return the dictionary entry as an RDF Turtle Document. Services must implement at least one of the `/json`, `/tei` or `/ontolex` actions.

### Example

```python
import time
import openapi_client
from openapi_client.api import default_api
from openapi_client.model.inline_response500 import InlineResponse500
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = default_api.DefaultApi(api_client)
    dictionary = "dictionary_example" # str | The dictionary containing the entry
    id = "id_example" # str | 
    x_api_key = "X-API-KEY_example" # str | An API key to authorize access to this endpoint if necessary (optional)

    # example passing only required values which don't have defaults set
    try:
        # Entry as Turtle
        api_instance.get_entry_as_onto_lex_by_id(dictionary, id)
    except openapi_client.ApiException as e:
        print("Exception when calling DefaultApi->get_entry_as_onto_lex_by_id: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Entry as Turtle
        api_instance.get_entry_as_onto_lex_by_id(dictionary, id, x_api_key=x_api_key)
    except openapi_client.ApiException as e:
        print("Exception when calling DefaultApi->get_entry_as_onto_lex_by_id: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **dictionary** | **str**| The dictionary containing the entry |
 **id** | **str**|  |
 **x_api_key** | **str**| An API key to authorize access to this endpoint if necessary | [optional]

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/turtle, application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  * last-modified - When this entry was last modified, formatted according to https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Last-Modified <br>  |
**301** | ID Updated (this entry has changed its ID) |  -  |
**403** | Forbidden (API key not specified or not valid) |  -  |
**404** | No Entry Availble (the dictionary or entry ID is not known or the entry has been deleted) |  -  |
**500** | Internal Server Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_entry_as_teiby_id**
> bool, date, datetime, dict, float, int, list, str, none_type get_entry_as_teiby_id(dictionary, id)

Entry XML

Return the TEI-Lex0 representation of the document. Services must implement at least one of the `/ontolex`, `/json` or `/tei` actions.

### Example

```python
import time
import openapi_client
from openapi_client.api import default_api
from openapi_client.model.inline_response500 import InlineResponse500
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = default_api.DefaultApi(api_client)
    dictionary = "dictionary_example" # str | The dictionary containing the entry
    id = "id_example" # str | 
    x_api_key = "X-API-KEY_example" # str | An API key to authorize access to this endpoint if necessary (optional)

    # example passing only required values which don't have defaults set
    try:
        # Entry XML
        api_response = api_instance.get_entry_as_teiby_id(dictionary, id)
        pprint(api_response)
    except openapi_client.ApiException as e:
        print("Exception when calling DefaultApi->get_entry_as_teiby_id: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Entry XML
        api_response = api_instance.get_entry_as_teiby_id(dictionary, id, x_api_key=x_api_key)
        pprint(api_response)
    except openapi_client.ApiException as e:
        print("Exception when calling DefaultApi->get_entry_as_teiby_id: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **dictionary** | **str**| The dictionary containing the entry |
 **id** | **str**|  |
 **x_api_key** | **str**| An API key to authorize access to this endpoint if necessary | [optional]

### Return type

**bool, date, datetime, dict, float, int, list, str, none_type**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/xml, application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  * last-modified - When this entry was last modified, formatted according to https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Last-Modified <br>  |
**301** | ID Updated (this entry has changed its ID) |  -  |
**403** | Forbidden (API key not specified or not valid) |  -  |
**404** | No Entry Availble (the dictionary or entry ID is not known or the entry has been deleted) |  -  |
**500** | Internal Server Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_entry_by_id**
> OntolexEntry get_entry_by_id(dictionary, id)

Entry as JSON

Return the Entry directly as a JSON document. Services must implement at least one of the `/json`, `/ontolex` or `/tei` actions.

### Example

```python
import time
import openapi_client
from openapi_client.api import default_api
from openapi_client.model.ontolex_entry import OntolexEntry
from openapi_client.model.inline_response500 import InlineResponse500
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = default_api.DefaultApi(api_client)
    dictionary = "dictionary_example" # str | The identifier of the dictionary containing the entry
    id = "id_example" # str | The identifier of the entry
    x_api_key = "X-API-KEY_example" # str | An API key to authorize access to this endpoint if necessary (optional)

    # example passing only required values which don't have defaults set
    try:
        # Entry as JSON
        api_response = api_instance.get_entry_by_id(dictionary, id)
        pprint(api_response)
    except openapi_client.ApiException as e:
        print("Exception when calling DefaultApi->get_entry_by_id: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Entry as JSON
        api_response = api_instance.get_entry_by_id(dictionary, id, x_api_key=x_api_key)
        pprint(api_response)
    except openapi_client.ApiException as e:
        print("Exception when calling DefaultApi->get_entry_by_id: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **dictionary** | **str**| The identifier of the dictionary containing the entry |
 **id** | **str**| The identifier of the entry |
 **x_api_key** | **str**| An API key to authorize access to this endpoint if necessary | [optional]

### Return type

[**OntolexEntry**](OntolexEntry.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  * last-modified - When this entry was last modified, formatted according to https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Last-Modified <br>  |
**301** | ID Updated (this entry has changed its ID) |  -  |
**403** | Forbidden (API key not specified or not valid) |  -  |
**404** | No Entry Availble (the dictionary or entry ID is not known or the entry has been deleted) |  -  |
**500** | Internal Server Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

