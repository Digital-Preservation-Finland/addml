# coding=utf-8
"""Utils for reading and writing ADDML data.
"""

import lxml.etree as ET
import xml_helpers.utils as h


ADDML_NS = 'http://www.arkivverket.no/standarder/addml'
NAMESPACES = {'addml': ADDML_NS,
              'xsi': h.XSI_NS}


def addml_ns(tag, prefix=""):
    """Adds ADDML namespace to tags"""
    path = '{%s}%s' % (ADDML_NS, tag)

    if prefix:
        tag = tag[0].upper() + tag[1:]
        return'{%s}%s%s' % (ADDML_NS, prefix, tag)
    return '{%s}%s' % (ADDML_NS, tag)


def _element(tag, prefix="", ns={}):
    """Return _ElementInterface with ADDML namespace.

    Prefix parameter is useful for adding prefixed to lower case tags.
    It just uppercases first letter of tag and appends it to prefix::

        element = _element('objectIdentifier', 'linking')
        element.tag
        'linkingObjectIdentifier'

    :tag: Tagname
    :prefix: Prefix for the tag (default="")
    :returns: ElementTree element object

    """
    ns['addml'] = ADDML_NS
    return ET.Element(addml_ns(tag, prefix), nsmap=ns)


def _subelement(parent, tag, prefix="", ns={}):
    """Return subelement for the given parent element. Created element
    is appended to parent element.

    :parent: Parent element
    :tag: Element tagname
    :prefix: Prefix for the tag
    :returns: Created subelement

    """
    ns['addml'] = ADDML_NS
    return ET.SubElement(parent, addml_ns(tag, prefix), nsmap=ns)


def addml(child_elements=None, namespaces=NAMESPACES):
    """
    """
    _addml = _element('addml', ns=namespaces)
    _addml.set(
        h.xsi_ns('schemaLocation'),
        'http://www.arkivverket.no/standarder/addml '
        'http://schema.arkivverket.no/ADDML/latest/addml.xsd')

    _dataset = _subelement(_addml, 'dataset')

    if child_elements:
        for elem in child_elements:
            _dataset.append(elem)

    return _addml


def iter_elements(starting_element, tag):
    """Iterate all element from starting element that match the `tag`
    parameter. Tag is always prefixed to ADDML namespace before
    matching.

    :starting_element: Element where matching elements are searched
    :returns: Generator object for iterating all elements

    """
    for elem in starting_element.findall('.//' + addml_ns(tag)):
        yield elem


def parse_name(section):
    """
    """
    return section.get('name')


def parse_reference(section):
    """
    """
    if section.tag == addml_ns('flatFile'):
        referencetype = 'definitionReference'
    else:
        referencetype = 'typeReference'

    return section.get(referencetype)


def iter_sections(addml_el, section):
    """
    """
    for elem in iter_elements(addml_el, section):
        yield elem


def sections_count(addml_el, section):
    """
    """
    return len([x for x in iter_sections(addml_el, section)])


def find_section_by_name(addml_el, section, name):
    """
    """
    for elem in iter_sections(addml_el, section):
        if elem.get('name') == name:
            return elem

    return None
