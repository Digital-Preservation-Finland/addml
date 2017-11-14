# coding=utf-8
"""Functions for reading and writing ADDML data.
"""

import os
import copy
import argparse
import sys

import lxml.etree as ET
from xml_helpers.utils import readfile, serialize

from siptools.utils import encode_path
from siptools_archives.techmd_utils.utils import create_techmdfile, \
        add_to_tempfile
from siptools_archives.techmd_utils.base import parse_name, parse_reference, \
        find_section_by_name, addml, sections_count, iter_sections, \
        iter_elements
from siptools_archives.techmd_utils.flatfiles import iter_flatfiles, \
        wrapper_elems, parse_charset, flatfiledefinition_count, \
        iter_flatfiledefinitions


def parse_arguments(arguments):
    """ Create arguments parser and return parsed command line
    arguments.
    """
    parser = argparse.ArgumentParser(description='Tool for '
                                     'modifying ADDML')
    parser.add_argument('package', type=str, help='Path to ADDML file')
    parser.add_argument('--workspace', dest='workspace', type=str,
                        default='./workspace', help="Workspace directory")

    return parser.parse_args(arguments)


def main(arguments=None):
    """The main method for argparser"""
    args = parse_arguments(arguments)
    relpath, path = check_addml_relpath(args.package)
    root = readfile(path).getroot()

    tempfile_root = ET.Element('contents')

    count = flatfiledefinition_count(root)
    for flatfiledef in iter_flatfiledefinitions(root):
        if count > 1:
            addmldata = create_new_addml(root, flatfiledef)
        name = parse_name(flatfiledef)
        reference = parse_reference(flatfiledef)
        techmdid = create_techmdfile(args.workspace, 'ADDML', '8.3',
                                     addmldata, name)

        for flatfile in iter_flatfiles(root):
            if parse_reference(flatfile) == reference:
                flatfilename = parse_name(flatfile)
                add_to_tempfile(tempfile_root, name, flatfilename,
                                'ADDML', relpath)

    tempfilename = encode_path('addml', suffix='file.xml')
    with open(os.path.join(args.workspace, tempfilename), 'w+') as outfile:
        outfile.write(serialize(tempfile_root))
        print "Wrote addml pairings to tempfile %s" % outfile.name

    return 0


def parse_addml(relpath, path, workspace):
    """The main method for argparser"""
    root = readfile(path).getroot()

    tempfile_root = ET.Element('contents')

    count = flatfiledefinition_count(root)
    for flatfiledef in iter_flatfiledefinitions(root):
        if count > 1:
            addmldata = create_new_addml(root, flatfiledef)
        name = parse_name(flatfiledef)
        reference = parse_reference(flatfiledef)
        techmdid = create_techmdfile(workspace, 'ADDML', '8.3',
                                     addmldata, name)

        for flatfile in iter_flatfiles(root):
            if parse_reference(flatfile) == reference:
                flatfilename = parse_name(flatfile)
                add_to_tempfile(tempfile_root, name, flatfilename,
                                'ADDML', relpath)

    tempfilename = encode_path('addml', suffix='file.xml')
    with open(os.path.join(workspace, tempfilename), 'w+') as outfile:
        outfile.write(serialize(tempfile_root))
        print "Wrote addml pairings to tempfile %s" % outfile.name

    return 0


def create_new_addml(root, flatfiledefinition):
    """Creates new addml metadata for each flatfile in the original addml
    metadata. Only the relevant sections from flatFileDefinitions,
    flatFileTypes and recordTypes are included in the new addml metadata
    as well as the fieldTypes section. The sections relevance is derived
    from reading the corresponding @typeReference and @name attributes
    from each section starting from the <flatFile> element.
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

    for root, dirs, files in os.walk(path):
        for filename in files:
            if filename == addml_filename:
                addml_relpath = os.path.relpath(root, path)
                if addml_relpath == '.':
                    addml_relpath = ''
                addml_path = os.path.join(path, addml_relpath, addml_filename)

                return addml_relpath, addml_path
    return False, False


def get_charset(path, filename):
    """
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

            return True, charset
    return False, None


if __name__ == '__main__':
    RETVAL = main()
    sys.exit(RETVAL)
