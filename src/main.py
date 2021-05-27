import time
import openapi_client
from openapi_client.api import default_api
from openapi_client.model.inline_response500 import InlineResponse500
from openapi_client.model.metadata import Metadata
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
        host = "http://localhost:8000"
)


if __name__ == "__main__":
    # Enter a context with an instance of the API client
    with openapi_client.ApiClient(configuration) as api_client:
        # Create an instance of the API class
        api_instance = default_api.DefaultApi(api_client)
        dictionary = "dictionary_example" # str | Identifier of the dictionary to describe

        # example passing only required values which don't have defaults set
        try:
            # About the dictionary
            api_response = api_instance.about(dictionary)
            pprint(api_response)
        except openapi_client.ApiException as e:
            print("Exception when calling DefaultApi->about: %s\n" % e)
