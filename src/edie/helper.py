from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from rdflib import Graph
from io import StringIO

def validate_tei(tei_entry) -> Element:
    return ElementTree.fromstring(tei_entry)


def validate_ontolex(ontolex_entry) -> Graph:
    g = Graph()
    g.parse(StringIO(ontolex_entry), format="n3")
    return g
