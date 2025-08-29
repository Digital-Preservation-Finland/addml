"""Utils for reading and writing ADDML data.
"""
from __future__ import annotations

from collections.abc import Generator, Iterable
from uuid import uuid4

import lxml.etree as ET
import xml_helpers.utils as h

from addml.base import NAMESPACES, _element, _subelement, iter_elements


def wrapper_elems(
    tag: str, child_elements: Iterable[ET._Element] | None = None
) -> ET._Element | None:
    """Creates addml wrapper elements with a supplied tag if it matches
    a value in the elems list. Appends child_elements if they are
    supplied.
    """
    elems = ['flatFiles', 'flatFileDefinitions', 'recordDefinitions',
             'fieldDefinitions', 'structureTypes', 'flatFileTypes',
             'recordTypes', 'fieldTypes', 'properties']
    if tag in elems:
        wrapper_el = _element(tag)
        if child_elements:
            for elem in child_elements:
                wrapper_el.append(elem)
        return wrapper_el
    return None


def definition_elems(
    tag: str,
    attname: str,
    reference: str | None = None,
    child_elements: Iterable[ET._Element] | None = None,
) -> ET._Element | None:
    """Creates addml definition elements with a supplied tag if it
    matches a value in the lists. The definition elements are addml
    elements that an be identified with the @name attribute. Most of
    the definition elements also carry reference attributes that link
    to an other definition element's @name. Appends child_elements if
    they are supplied.
    """
    elems = ['flatFile', 'flatFileDefinition', 'recordDefinition']
    ref_elems = ['flatFile', 'fieldDefinition']
    noref_elems = ['flatFileType', 'recordType', 'fieldType', 'property']
    if tag in elems or tag in ref_elems or tag in noref_elems:
        definition_el_ = _element(tag)
        definition_el_.set('name', attname)

        if tag in ref_elems and not reference:
            reference = str(uuid4())
        if tag in noref_elems:
            reference = None

        if tag == 'flatFile':
            definition_el_.set('definitionReference', reference)
        elif reference:
            definition_el_.set('typeReference', reference)

        if child_elements:
            for elem in child_elements:
                definition_el_.append(elem)

        return definition_el_

    return None


def addml_basic_elem(tag: str, contents: str) -> ET._Element | None:
    """Creates ADDML basic elems that are elements which
    contain text as values. Only create elements if the supplied tag
    value is inlcuded in the tags list.
    """
    tags = ['charset', 'dataType']
    if tag in tags:
        addml_el = _element(tag)
        addml_el.text = h.decode_utf8(contents)
        return addml_el
    return None


def delimfileformat(
    recordseparator: str,
    fieldseparatingchar: str,
    quotingchar: str | None = None,
) -> ET._Element:
    """Creates the ADDML delimFileFormat section.

    :param recordseparator: the character separating the records
    :param fieldseparatingchar: the character separating the fields
    :param quotingchar: the quoting character used around the
    fields (default=None)

    :returns:
    The following lxml.etree strucure::

        <addml:delimFileFormat>
            <addml:recordSeparator>CR+LF</addml:recordSeparator>
            <addml:fieldSeparatingChar>;</addml:fieldSeparatingChar>
            <addml:quotingChar>'</addml:quotingChar>
        </addml:delimFileFormat>s
    """
    delimfileformat_el = _element('delimFileFormat')

    recordseparator_el = _subelement(delimfileformat_el, 'recordSeparator')
    recordseparator_el.text = h.decode_utf8(recordseparator)

    fieldseparatingchar_el = _subelement(delimfileformat_el,
                                         'fieldSeparatingChar')
    fieldseparatingchar_el.text = h.decode_utf8(fieldseparatingchar)

    if quotingchar:
        quotingchar_el = _subelement(delimfileformat_el, 'quotingChar')
        quotingchar_el.text = h.decode_utf8(quotingchar)

    return delimfileformat_el


def iter_flatfiles(addml_el: ET._Element) -> Generator[ET._Element]:
    """Iterates all flatFiles from starting element."""
    yield from iter_elements(addml_el, 'flatFile')


def iter_flatfiledefinitions(addml_el: ET._Element) -> Generator[ET._Element]:
    """Iterates all flatFileDefinitions from starting element."""
    yield from iter_elements(addml_el, 'flatFileDefinition')


def flatfile_count(addml_el: ET._Element) -> int:
    """Returns number of flatFiles in addml data."""
    return len(list(iter_flatfiles(addml_el)))


def flatfiledefinition_count(addml_el: ET._Element) -> int:
    """Returns number of flatFileDefinitions in addml data."""
    return len(list(iter_flatfiledefinitions(addml_el)))


def parse_charset(section: ET._Element) -> str:
    """Returns the value of the charset within a given section."""
    return h.decode_utf8(section.xpath(".//addml:charset/text()",
                                       namespaces=NAMESPACES)[0])
