"""Utils for reading and writing ADDML data.
"""

import lxml.etree as ET
import xml_helpers.utils as h

ADDML_NS = 'http://www.arkivverket.no/standarder/addml'
NAMESPACES = {'addml': ADDML_NS,
              'xsi': h.XSI_NS}


def addml_ns(tag, prefix=""):
    """Adds ADDML namespace to tags"""
    if prefix:
        tag = tag[0].upper() + tag[1:]
        return '{{{}}}{}{}'.format(ADDML_NS, prefix, tag)
    return '{{{}}}{}'.format(ADDML_NS, tag)


# TODO: Rename this element when doing actual refactoring,
#       because this is used in other modules as well.
# TODO: When doing actual refactoring, resolve redefined-outer-name warning.
def _element(tag, prefix="", ns=None):
    """Return _ElementInterface with ADDML namespace.

    Prefix parameter is useful for adding prefixed to lower case tags.
    It just uppercases first letter of tag and appends it to prefix::

        element = _element('definition', 'flatFile')
        element.tag
        'flatFileDefinition'

    :tag: Tagname
    :prefix: Prefix for the tag (default="")
    :returns: ElementTree element object

    """
    if ns is None:
        ns = {}
    ns['addml'] = ADDML_NS
    return ET.Element(addml_ns(tag, prefix), nsmap=ns)


# TODO: Rename this element when doing actual refactoring,
#       because this is used in other modules as well.
# TODO: When doing actual refactoring, resolve redefined-outer-name warning.
def _subelement(parent, tag, prefix="", ns=None):
    """Return subelement for the given parent element. Created element
    is appended to parent element.

    :parent: Parent element
    :tag: Element tagname
    :prefix: Prefix for the tag
    :returns: Created subelement

    """
    if ns is None:
        ns = {}
    ns['addml'] = ADDML_NS
    return ET.SubElement(parent, addml_ns(tag, prefix), nsmap=ns)


def addml(child_elements=None, namespaces=None):
    """Creates an addml root element with correct namespace definition
    and schemalocation attributes. Also creates the mandatory
    <addml:dataset> element within the root element.
    """
    if namespaces is None:
        namespaces = NAMESPACES
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
    yield from starting_element.findall('.//' + addml_ns(tag))


def parse_name(section):
    """Returns the value of the @name attribute of an element."""
    return section.get('name')


def parse_reference(section):
    """Returns the value of the reference attribute of an element.
    The reference attribute is either @definitionReference if the
    element is a <flatFile> or @typeReference for other elements.
    """
    if section.tag == addml_ns('flatFile'):
        referencetype = 'definitionReference'
    else:
        referencetype = 'typeReference'

    return section.get(referencetype)


def iter_sections(addml_el, section):
    """Iterate all addml data sections from starting element."""
    yield from iter_elements(addml_el, section)


def sections_count(addml_el, section):
    """Return number of sections in ADDML data."""
    return len([x for x in iter_sections(addml_el, section)])


def find_section_by_name(addml_el, section, name):
    """Find an addml section by its @name attribute value."""
    for elem in iter_sections(addml_el, section):
        if elem.get('name') == name:
            return elem

    return None
