"""Test for the ADDML flatFiles class."""

import lxml.etree as ET
import xml_helpers.utils as h
import addml.base as a
import addml.flatfiles as f


def test_wrapper_elems_ok():
    """Tests the wrapper_elems function by comparing test data output
    with a predefined string.
    """
    xml = """<addml:flatFiles
    xmlns:addml="http://www.arkivverket.no/standarder/addml"><addml:flatFile
    name="file1" definitionReference="def1"></addml:flatFile><addml:flatFile
    name="file2" definitionReference="def2"></addml:flatFile><addml:flatFile
    name="file3"
    definitionReference="def3"></addml:flatFile></addml:flatFiles>"""
    file1 = f.definition_elems('flatFile', 'file1', reference='def1')
    file2 = f.definition_elems('flatFile', 'file2', reference='def2')
    file3 = f.definition_elems('flatFile', 'file3', reference='def3')
    wrapper_elem = f.wrapper_elems('flatFiles', child_elements=[file1, file2,
                                                                file3])
    assert h.compare_trees(ET.fromstring(xml), wrapper_elem) is True


def test_wrapper_elems_fail():
    """Tests that the wrapper_elems function doesn't write
    data if the supplied tag is unsupported.
    """
    file1 = f.definition_elems('flatFile', 'file1', reference='def1')
    wrapper_elem = f.wrapper_elems('flatFyles', child_elements=[file1])
    assert wrapper_elem is None


def test_definition_elems_flatfile():
    """Tests the definition_elems function by comparing test data output
    with a predefined string.
    """
    xml = """<addml:flatFile
    xmlns:addml="http://www.arkivverket.no/standarder/addml"
    name="file1" definitionReference="def1"><addml:properties><addml:property
    name="prop1"></addml:property></addml:properties></addml:flatFile>"""
    fprop = f.definition_elems('property', 'prop1')
    fprops = f.wrapper_elems('properties', child_elements=[fprop])
    ffile = f.definition_elems('flatFile', 'file1',
                               reference='def1',
                               child_elements=[fprops])

    assert h.compare_trees(ET.fromstring(xml), ffile) is True


def test_definition_elems_noname():
    """Tests that the definition_elems function writes the
    definitionReference or typeReference attribute to an element if it
    isn't supplied but is mandatory.
    """
    fidef = f.definition_elems('fieldDefinition', 'fidef1')

    assert list(fidef.attrib.keys()) == ['name', 'typeReference']
    assert len(fidef.get('typeReference')) > 0


def test_definition_elems_removeref():
    """Tests that the definition_elems function doesn't write an
    typeReference if it is forbidden in the element.
    """
    fftype = f.definition_elems('flatFileType', 'type1', reference='test')

    assert list(fftype.attrib.keys()) == ['name']


def test_definition_elems_fail():
    """Tests that the definition_elems function doesn't write
    data if the supplied tag is unsupported.
    """
    file1 = f.definition_elems('flatFyle', 'file1', reference='def1')
    assert file1 is None


def test_addml_basic_elem():
    """Tests the addml_basic_elem function by comparing the function
    output with a predifined string.
    """
    xml = """<addml:charset
    xmlns:addml="http://www.arkivverket.no/standarder/addml"
    >UTF-8</addml:charset>"""
    charset = f.addml_basic_elem('charset', 'UTF-8')
    assert h.compare_trees(ET.fromstring(xml), charset) is True


def test_addml_basic_elem_fail():
    """Tests that the addml_basic_elem function doesn't write
    data if input tag is unsupported.."""
    fail = f.addml_basic_elem('test', 'test')
    assert fail is None


def test_delimfileformat():
    """Tests the delimfileformat function by comparing the function
    output with a predifined string.
    """
    xml = """<addml:delimFileFormat
    xmlns:addml="http://www.arkivverket.no/standarder/addml"
    ><addml:recordSeparator>CR+LF</addml:recordSeparator
    ><addml:fieldSeparatingChar>;</addml:fieldSeparatingChar
    ><addml:quotingChar>'</addml:quotingChar></addml:delimFileFormat>"""
    charset = f.delimfileformat('CR+LF', ';', quotingchar="'")
    assert h.compare_trees(ET.fromstring(xml), charset) is True


def test_iter_flatfiles():
    """Test iter_flatfiles by asserting that only the
    relevant sections are iterated through from the testdata.
    """
    file1 = f.definition_elems('flatFile', 'file1', reference='def1')
    file2 = f.definition_elems('flatFile', 'file2', reference='def2')
    file3 = f.definition_elems('flatFile', 'file3', reference='def3')
    def1 = f.definition_elems('flatFileDefinition', 'def1', reference='type1')
    def2 = f.definition_elems('flatFileDefinition', 'def2', reference='type2')
    xml = a.addml(child_elements=[file1, file2, file3, def1, def2])
    i = 0
    for iter_elem in f.iter_flatfiles(xml):
        i = i + 1
        assert iter_elem.get('name') == 'file' + str(i)
    assert i == 3


def test_iter_flatfiledefinitions():
    """Test iter_flatfiledefinitions by asserting that only the
    relevant sections are iterated through from the testdata.
    """
    file1 = f.definition_elems('flatFile', 'file1', reference='def1')
    file2 = f.definition_elems('flatFile', 'file2', reference='def2')
    file3 = f.definition_elems('flatFile', 'file3', reference='def3')
    def1 = f.definition_elems('flatFileDefinition', 'def1', reference='type1')
    def2 = f.definition_elems('flatFileDefinition', 'def2', reference='type2')
    xml = a.addml(child_elements=[file1, file2, file3, def1, def2])
    i = 0
    for iter_elem in f.iter_flatfiledefinitions(xml):
        i = i + 1
        assert iter_elem.get('name') == 'def' + str(i)
    assert i == 2


def test_flatfile_count():
    """Test flatfile_count by asserting that the number of
    counted sections matches the testdata.
    """
    file1 = f.definition_elems('flatFile', 'file1', reference='def1')
    file2 = f.definition_elems('flatFile', 'file2', reference='def2')
    file3 = f.definition_elems('flatFile', 'file3', reference='def3')
    def1 = f.definition_elems('flatFileDefinition', 'def1', reference='type1')
    def2 = f.definition_elems('flatFileDefinition', 'def2', reference='type2')
    xml = a.addml(child_elements=[file1, file2, file3, def1, def2])
    assert f.flatfile_count(xml) == 3


def test_flatfiledefinition_count():
    """Test flatfiledefinition_count by asserting that the number of
    counted sections matches the testdata.
    """
    file1 = f.definition_elems('flatFile', 'file1', reference='def1')
    file2 = f.definition_elems('flatFile', 'file2', reference='def2')
    file3 = f.definition_elems('flatFile', 'file3', reference='def3')
    def1 = f.definition_elems('flatFileDefinition', 'def1', reference='type1')
    def2 = f.definition_elems('flatFileDefinition', 'def2', reference='type2')
    xml = a.addml(child_elements=[file1, file2, file3, def1, def2])
    assert f.flatfiledefinition_count(xml) == 2


def test_parse_charset():
    """Test the parse_charset function by asserting the output value
    from addml data.
    """
    charset = f.addml_basic_elem('charset', 'UTF-8')
    fftype = f.wrapper_elems('flatFileTypes', child_elements=[charset])
    xml = a.addml(child_elements=[fftype])

    assert f.parse_charset(xml) == 'UTF-8'
