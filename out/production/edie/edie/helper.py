from xml.etree import ElementTree
from xml.etree.ElementTree import Element


def validate_tei(tei_entry) -> Element:
    return ElementTree.fromstring(tei_entry)