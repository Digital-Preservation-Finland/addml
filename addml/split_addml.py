"""Functions for reading and writing ADDML data.
"""

import copy
import os

from addml.base import (addml, find_section_by_name, iter_sections, parse_name,
                        parse_reference)
from addml.flatfiles import (flatfiledefinition_count,
                             iter_flatfiledefinitions, iter_flatfiles,
                             parse_charset, wrapper_elems)
from xml_helpers.utils import readfile


def parse_flatfiledefinitions(path):
    """Parses ADDML data and splits the data into new ADDML data
    files for each flatFileDefinition in the original data file.
    Returns the ADDML data for each created file.
    """
    root = readfile(path).getroot()
    addmldata = root
    count = flatfiledefinition_count(root)

    for flatfiledef in iter_flatfiledefinitions(root):
        if count > 1:
            addmldata = create_new_addml(root, flatfiledef)

        yield addmldata


def parse_flatfilenames(path, reference):
    """Returns the @name attribute for each flatFile whose
    @definitionReference attribute value matches the supplied value.
    """
    root = readfile(path).getroot()

    for flatfile in iter_flatfiles(root):
        if parse_reference(flatfile) == reference:
            flatfilename = parse_name(flatfile)

            yield flatfilename


def create_new_addml(root, flatfiledefinition):
    """Creates new addml metadata for each flatFileDefinition in the
    original addml metadata. Only the relevant sections from flatFiles,
    flatFileTypes and recordTypes are included in the new addml metadata
    as well as the fieldTypes section. The sections relevance is derived
    from reading the corresponding @typeReference and @name attributes
    from each section starting from the <flatFileDefinition> element.
    """
    flatfiles_list = []

    namereference = parse_name(flatfiledefinition)
    for flatfile in iter_flatfiles(root):
        if parse_reference(flatfile) == namereference:
            flatfiles_list.append(copy.deepcopy(flatfile))

    typereference = parse_reference(flatfiledefinition)
    flatfiledefinitions = wrapper_elems(
        'flatFileDefinitions',
        child_elements=[copy.deepcopy(flatfiledefinition)])
    flatfiles_list.append(flatfiledefinitions)

    structuretypes_list = []

    flatfiletype = find_section_by_name(root, 'flatFileType', typereference)
    flatfiletypes = wrapper_elems(
        'flatFileTypes', child_elements=[copy.deepcopy(flatfiletype)])
    structuretypes_list.append(flatfiletypes)

    for recorddefinition in iter_sections(flatfiledefinitions,
                                          'recordDefinition'):
        if parse_reference(recorddefinition):
            recordtype = find_section_by_name(
                root, 'recordType', parse_reference(recorddefinition))
            recordtypes = wrapper_elems(
                'recordTypes', child_elements=[copy.deepcopy(recordtype)])
            structuretypes_list.append(recordtypes)

    for fieldtypes in iter_sections(root, 'fieldTypes'):
        structuretypes_list.append(copy.deepcopy(fieldtypes))

    structuretypes = wrapper_elems('structureTypes',
                                   child_elements=structuretypes_list)
    flatfiles_list.append(structuretypes)
    flatfiles = wrapper_elems('flatFiles',
                              child_elements=flatfiles_list)

    addmldata = addml(child_elements=[flatfiles])

    return addmldata


def check_addml_relpath(path):
    """Checks if an ADDML file exists within the package. Returns the
    relative path of the ADDML file if one is found, otherwise returns
    False.
    """

    addml_filename = 'addml.xml'

    for root, _, files in os.walk(path):
        for filename in files:
            if filename == addml_filename:
                addml_relpath = os.path.relpath(root, path)
                if addml_relpath == '.':
                    addml_relpath = ''
                addml_path = os.path.join(path, addml_relpath, addml_filename)

                return addml_relpath, addml_path
    return False, False


def get_charset_with_filename(path, filename):
    """Returns the charset from the ADDML data for a given file. The
    filename is matched against the @name attribute for each flatFile
    element and the correct charset is returned from the correct
    flatFileType section that matches the flatFile.
    """
    root = readfile(path).getroot()
    for flatfile in iter_flatfiles(root):
        if parse_name(flatfile) == filename:
            def_reference = parse_reference(flatfile)
            definition = find_section_by_name(root, 'flatFileDefinition',
                                              def_reference)
            type_reference = parse_reference(definition)
            flatfiletype = find_section_by_name(root, 'flatFileType',
                                                type_reference)
            charset = 'charset=%s' % parse_charset(flatfiletype)

            return charset
    return None
