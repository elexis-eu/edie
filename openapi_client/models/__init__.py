# flake8: noqa

# import all models into this package
# if you have many models here with many references from one model to another this may
# raise a RecursionError
# to avoid this, import only the models that you directly need like:
# from from openapi_client.model.pet import Pet
# or import this package, but before doing it, use:
# import sys
# sys.setrecursionlimit(n)

from openapi_client.model.agent import Agent
from openapi_client.model.agent_class import AgentClass
from openapi_client.model.entry import Entry
from openapi_client.model.inline_response200 import InlineResponse200
from openapi_client.model.inline_response500 import InlineResponse500
from openapi_client.model.metadata import Metadata
from openapi_client.model.ontolex_entry import OntolexEntry
from openapi_client.model.ontolex_entry_canonical_form import OntolexEntryCanonicalForm
from openapi_client.model.ontolex_form import OntolexForm
from openapi_client.model.ontolex_lexical_sense import OntolexLexicalSense
