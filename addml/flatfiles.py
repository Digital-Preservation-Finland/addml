# coding=utf-8
"""Utils for reading and writing ADDML data.
"""

from uuid import uuid4

import xml_helpers.utils as h

from siptools_archives.techmd_utils.base import _element, _subelement, \
        iter_elements, NAMESPACES


def wrapper_elems(tag, child_elements=None):
    """
    """
    elems = ['flatFiles', 'flatFileDefinitions', 'recordDefinitions',
             'fieldDefinitions', 'structureTypes', 'flatFileTypes',
             'recordTypes', 'fieldTypes']
    if tag in elems:
        wrapper_el = _element(tag)
        if child_elements:
            for elem in child_elements:
                wrapper_el.append(elem)
        return wrapper_el
    return None


def definition_elems(tag, name, reference=None, child_elements=None):
    """
    """
    elems = ['flatFile', 'flatFileDefinition', 'recordDefinition']
    ref_elems = ['flatFile', 'fieldDefinition']
    noref_elems = ['flatFileType', 'recordType', 'fieldType']
    if tag in elems or tag in ref_elems or tag in noref_elems:
        definition_el = _element(tag)
        definition_el.set = ('name', name)

        if tag in ref_elems and not reference:
            reference = str(uuid4)
        if tag in noref_elems:
            reference = None

        if tag == 'flatFile':
            definition_el.set('definitionReference', reference)
        else:
            if reference:
                definition_el.set('typeReference', reference)

        if child_elements:
            for elem in child_elements:
                definition_el.append(elem)

        return definition_el

    return None


def addml_basic_elem(tag, contents):
    """
    """
    tags = ['charset', 'dataType']
    if tag in tags:
        addml_el = _element(tag)
        addml_el.text = h.decode_utf8(contents)
        return addml_el
    return None


def delimfileformat(recordseparator, fieldseparatingchar, quotingchar=None):
    """
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
    """
    """
    for elem in iter_elements(addml_el, 'flatFile'):
        yield elem


def iter_flatfiledefinitions(addml_el):
    """
    """
    for elem in iter_elements(addml_el, 'flatFileDefinition'):
        yield elem


def flatfile_count(addml_el):
    """
    """
    return len([x for x in iter_flatfiles(addml_el)])


def flatfiledefinition_count(addml_el):
    """
    """
    return len([x for x in iter_flatfiledefinitions(addml_el)])


def parse_charset(section):
    """
    """
    return h.encode_utf8(section.xpath(".//addml:charset/text()",
                                       namespaces=NAMESPACES)[0])
