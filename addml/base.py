"""Utils for reading and writing ADDML data.
"""
from __future__ import annotations

from collections.abc import Generator, Iterable

import lxml.etree as ET
import xml_helpers.utils as h

ADDML_NS = 'http://www.arkivverket.no/standarder/addml'
NAMESPACES = {'addml': ADDML_NS,
              'xsi': h.XSI_NS}


def addml_ns(tag: str, prefix: str = "") -> str:
    """Adds ADDML namespace to tags"""
    if prefix:
        tag = tag[0].upper() + tag[1:]
        return f'{{{ADDML_NS}}}{prefix}{tag}'
    return f'{{{ADDML_NS}}}{tag}'


# TODO: Rename this element when doing actual refactoring,
#       because this is used in other modules as well.
# TODO: When doing actual refactoring, resolve redefined-outer-name warning.
def _element(
    tag: str, prefix: str = "", ns: dict[str, str] | None = None
) -> ET._Element:
    """Return _ElementInterface with ADDML namespace.

    Prefix parameter is useful for adding prefixed to lower case tags.
    It just uppercases first letter of tag and appends it to prefix::

        element = _element('definition', 'flatFile')
        element.tag
        'flatFileDefinition'

    :param tag: Tagname
    :param prefix: Prefix for the tag (default="")
    :param ns: Namespace
    :returns: ElementTree element object

    """
    if ns is None:
        ns = {}
    ns['addml'] = ADDML_NS
    return ET.Element(addml_ns(tag, prefix), nsmap=ns)


# TODO: Rename this element when doing actual refactoring,
#       because this is used in other modules as well.
# TODO: When doing actual refactoring, resolve redefined-outer-name warning.
def _subelement(
    parent: ET._Element,
    tag: str,
    prefix: str = "",
    ns: dict[str, str] | None = None,
) -> ET._Element:
    """Return subelement for the given parent element. Created element
    is appended to parent element.

    :param parent: Parent element
    :param tag: Element tagname
    :param prefix: Prefix for the tag
    :param ns: Namespace
    :returns: Created subelement

    """
    if ns is None:
        ns = {}
    ns['addml'] = ADDML_NS
    return ET.SubElement(parent, addml_ns(tag, prefix), nsmap=ns)


def addml(
    child_elements: Iterable[ET._Element] | None = None,
    namespaces: dict[str, str] | None = None,
) -> ET._Element:
    """Creates an addml root element with correct namespace definition
    and schemalocation attributes. Also creates the mandatory
    <addml:dataset> element within the root element.

    :param child_elements: Iterable of elements
    :param namespaces: Namespace to use
    :returns: Addml root element
    """
    if namespaces is None:
        namespaces = NAMESPACES
    addml_ = _element('addml', ns=namespaces)
    addml_.set(
        h.xsi_ns('schemaLocation'),
        'http://www.arkivverket.no/standarder/addml '
        'http://schema.arkivverket.no/ADDML/latest/addml.xsd')

    dataset_ = _subelement(addml_, 'dataset')

    if child_elements:
        for elem in child_elements:
            dataset_.append(elem)

    return addml_


def iter_elements(
    starting_element: ET._Element, tag: str
) -> Generator[ET._Element]:
    """Iterate all element from starting element that match the `tag`
    parameter. Tag is always prefixed to ADDML namespace before
    matching.

    :param starting_element: Element where matching elements are searched
    :param tag: String tag
    :returns: Generator object for iterating all elements

    """
    yield from starting_element.findall('.//' + addml_ns(tag))


def parse_name(section: ET._Element) -> str:
    """Returns the value of the @name attribute of an element."""
    return section.get('name')


def parse_reference(section: ET._Element) -> str:
    """Returns the value of the reference attribute of an element.
    The reference attribute is either @definitionReference if the
    element is a <flatFile> or @typeReference for other elements.
    """
    if section.tag == addml_ns('flatFile'):
        referencetype = 'definitionReference'
    else:
        referencetype = 'typeReference'

    return section.get(referencetype)


def iter_sections(
    addml_el: ET._Element, section: str
) -> Generator[ET._Element]:
    """Iterate all addml data sections from starting element."""
    yield from iter_elements(addml_el, section)


def sections_count(addml_el: ET._Element, section: str) -> int:
    """Return number of sections in ADDML data."""
    return len(list(iter_sections(addml_el, section)))


def find_section_by_name(
    addml_el: ET._Element, section: str, name: str
) -> ET._Element | None:
    """Find an addml section by its @name attribute value."""
    for elem in iter_sections(addml_el, section):
        if elem.get('name') == name:
            return elem

    return None
