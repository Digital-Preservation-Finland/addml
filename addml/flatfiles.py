# coding=utf-8
"""Utils for reading and writing ADDML data.
"""
from __future__ import unicode_literals

from uuid import uuid4

import xml_helpers.utils as h
from addml.base import NAMESPACES, _element, _subelement, iter_elements


def wrapper_elems(tag, child_elements=None):
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


def definition_elems(tag, attname, reference=None, child_elements=None):
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
        _definition_el = _element(tag)
        _definition_el.set('name', attname)

        if tag in ref_elems and not reference:
            reference = str(uuid4())
        if tag in noref_elems:
            reference = None

        if tag == 'flatFile':
            _definition_el.set('definitionReference', reference)
        else:
            if reference:
                _definition_el.set('typeReference', reference)

        if child_elements:
            for elem in child_elements:
                _definition_el.append(elem)

        return _definition_el

    return None


def addml_basic_elem(tag, contents):
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


def delimfileformat(recordseparator, fieldseparatingchar, quotingchar=None):
    """Creates the ADDML delimFileFormat section.

    :recordseparator: the charcter separating the records
    :fieldseparatingchar: the character separating the fields
    :quotingchar: the quoting character used around the
    fields (default=None)

    Returns the following lxml.etree strucure:
        <addml:delimFileFormat>
            <addml:recordSeparator>CR+LF</addml:recordSeparator>
            <addml:fieldSeparatingChar>;</addml:fieldSeparatingChar>
            <addml:quotingChar>'</addml:quotingChar>
        </addml:delimFileFormat>
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


def iter_flatfiles(addml_el):
    """Iterates all flatFiles from starting element."""
    for elem in iter_elements(addml_el, 'flatFile'):
        yield elem


def iter_flatfiledefinitions(addml_el):
    """Iterates all flatFileDefinitions from starting element."""
    for elem in iter_elements(addml_el, 'flatFileDefinition'):
        yield elem


def flatfile_count(addml_el):
    """Returns number of flatFiles in addml data."""
    return len([x for x in iter_flatfiles(addml_el)])


def flatfiledefinition_count(addml_el):
    """Returns number of flatFileDefinitions in addml data."""
    return len([x for x in iter_flatfiledefinitions(addml_el)])


def parse_charset(section):
    """Returns the value of the charset within a given section."""
    return h.decode_utf8(section.xpath(".//addml:charset/text()",
                                       namespaces=NAMESPACES)[0])
