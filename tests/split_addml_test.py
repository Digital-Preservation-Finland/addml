"""Test for the ADDML flatFiles class."""
from __future__ import unicode_literals

import six

import addml.base as a
import addml.flatfiles as f
import addml.split_addml as s
import xml_helpers.utils as h


def test_parse_flatfiledefinitions_simple():
    """Tests the parse_flatfiledefinitions function by supplying
    testdata to the function and asserting that the correct number of
    ADDML sections are returned per addmldata. Also asserts that the
    correct number of addml data files are returned.
    """
    addml = 'tests/data/addml_simple.xml'
    i = 0
    for addmls in s.parse_flatfiledefinitions(addml):
        i = i + 1
        assert f.flatfile_count(addmls) == 1
        assert f.flatfiledefinition_count(addmls) == 1
        assert a.sections_count(addmls, 'flatFileType') == 1
        assert a.sections_count(addmls, 'recordType') == 1
        assert a.sections_count(addmls, 'fieldTypes') == 1
    assert i == 1


def test_parse_flatfiledefinitions_medium():
    """Tests the parse_flatfiledefinitions function by supplying
    testdata to the function and asserting that the correct number of
    ADDML sections are returned per addmldata. Also asserts that the
    correct number of addml data files are returned and that the
    sections have correct name attributes.
    """
    addml = 'tests/data/addml_medium.xml'
    i = 0
    for addmls in s.parse_flatfiledefinitions(addml):
        i = i + 1
        assert f.flatfile_count(addmls) == 1
        assert f.flatfiledefinition_count(addmls) == 1
        assert a.sections_count(addmls, 'flatFileType') == 1
        assert a.sections_count(addmls, 'recordType') == 1
        assert a.sections_count(addmls, 'fieldTypes') == 1
        for flatfile in f.iter_flatfiles(addmls):
            assert \
                a.parse_name(flatfile) == 'csvfile' + six.text_type(i) + '.csv'
    assert i == 3


def test_parse_flatfiledefinitions_complex():
    """Tests the parse_flatfiledefinitions function by supplying
    testdata to the function and asserting that the correct number of
    ADDML sections are returned per addmldata. Also asserts that the
    correct number of addml data files are returned and that the
    sections have correct name attributes and that various elements
    contain right data for each addml data file respectively.
    """
    addml = 'tests/data/addml_complex.xml'
    i = 0
    for addmls in s.parse_flatfiledefinitions(addml):
        i = i + 1
        assert f.flatfiledefinition_count(addmls) == 1
        assert a.sections_count(addmls, 'flatFileType') == 1
        assert a.sections_count(addmls, 'recordType') == 1
        assert a.sections_count(addmls, 'fieldTypes') == 1
        for ffdef in f.iter_flatfiledefinitions(addmls):
            assert a.parse_name(ffdef) == 'testdef' + six.text_type(i)
            if a.parse_name(ffdef) == 'testdef1':
                assert f.flatfile_count(addmls) == 3
                assert f.parse_charset(addmls) == 'UTF-8'
                assert a.sections_count(addmls, 'fieldDefinition') == 3
            elif a.parse_name(ffdef) == 'testdef2':
                assert f.flatfile_count(addmls) == 2
                assert f.parse_charset(addmls) == 'ISO-8859-15'
                assert a.sections_count(addmls, 'fieldDefinition') == 2
            elif a.parse_name(ffdef) == 'testdef3':
                assert f.flatfile_count(addmls) == 1
                assert f.parse_charset(addmls) == 'ASCII'
                assert a.sections_count(addmls, 'fieldDefinition') == 3
    assert i == 3


def test_parse_flatfilenames():
    """Tests the parse_flatfilenames function by asserting that the function
    returns the name attribute for each flatFile according to the
    supplied definitionReference attribute value. Also asserts that the
    correct number of flatFile elements' names are returned.
    """
    addml = 'tests/data/addml_complex.xml'
    i = 0
    for ffname in s.parse_flatfilenames(addml, 'testdef1'):
        i = i + 1
        assert ffname[:7] == 'csvfile'
        assert ffname[-4:] == '.csv'
        assert len(ffname) == 12
    assert i == 3


def test_create_new_addml_simple():
    """Tests the create_new_addml function by supplying testdata to the
    function and asserting that the correct number of ADDML sections are
    returned.
    """
    addml = 'tests/data/addml_simple.xml'
    root = h.readfile(addml)
    for ffdef in f.iter_flatfiledefinitions(root):
        testdef = ffdef
    addml_new = s.create_new_addml(root, testdef)
    assert f.flatfile_count(addml_new) == 1
    assert f.flatfiledefinition_count(addml_new) == 1
    assert a.sections_count(addml_new, 'flatFileType') == 1
    assert a.sections_count(addml_new, 'recordType') == 1
    assert a.sections_count(addml_new, 'fieldTypes') == 1


def test_create_new_addml_complex():
    """Tests the create_new_addml function by supplying testdata to the
    function and asserting that the correct number of ADDML sections are
    returned and that various elements contain the correct data.
    """
    addml = 'tests/data/addml_complex.xml'
    root = h.readfile(addml)
    for ffdef in f.iter_flatfiledefinitions(root):
        testdef = a.find_section_by_name(root, 'flatFileDefinition',
                                         'testdef2')
    addml_new = s.create_new_addml(root, testdef)
    assert f.flatfile_count(addml_new) == 2
    assert f.flatfiledefinition_count(addml_new) == 1
    assert a.sections_count(addml_new, 'flatFileType') == 1
    assert a.sections_count(addml_new, 'recordType') == 1
    assert a.sections_count(addml_new, 'fieldTypes') == 1
    assert f.flatfile_count(addml_new) == 2
    assert f.parse_charset(addml_new) == 'ISO-8859-15'
    assert a.sections_count(addml_new, 'fieldDefinition') == 2


def test_get_charset_with_filename():
    """Asserts that the function get_charset_with_filename returns the
    correct value from an ADDML data file and returns it with the string
    'charset=' applied to it.
    """
    addml = 'tests/data/addml_complex.xml'
    charset = s.get_charset_with_filename(addml, 'csvfile3.csv')
    assert charset == 'charset=ASCII'


def test_get_charset_with_filename_nofile():
    """Tests that the get_charset_with_filename returns None if no
    flatfile was found with the supplied filename.
    """
    addml = 'tests/data/addml_complex.xml'
    charset = s.get_charset_with_filename(addml, 'csvfile7.csv')
    assert charset is None
