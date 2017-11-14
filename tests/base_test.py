"""Test for the ADDML class."""

import lxml.etree as ET
import xml_helpers.utils as h
import addml.base as a
import addml.flatfiles as f


def test_addml_ns():
    """Test premis_ns"""
    assert a.addml_ns('xxx') == '{http://www.arkivverket.no/standarder/addml}xxx'


def test_element():
    """Test ADDML _element"""
    xml = """<addml:xxx xmlns:addml="http://www.arkivverket.no/standarder/addml"/>"""
    assert h.compare_trees(a._element('xxx'), ET.fromstring(xml)) == True


def test_subelement():
    """Test ADDML _subelement"""
    xml = """<addml:xxx xmlns:addml="http://www.arkivverket.no/standarder/addml"/>"""
    parent_xml = """<addml:addml xmlns:addml="http://www.arkivverket.no/standarder/addml"/>"""
    parent = ET.fromstring(parent_xml)
    assert h.compare_trees(a._subelement(parent, 'xxx'), ET.fromstring(xml)) == True


def test_addml():
    """Test ADDML root generation"""
    tree = ET.tostring(a.addml())
    xml = """<addml:addml
            xsi:schemaLocation="http://www.arkivverket.no/standarder/addml http://schema.arkivverket.no/ADDML/latest/addml.xsd"
            xmlns:addml = "http://www.arkivverket.no/standarder/addml"
            xmlns:xsi = "http://www.w3.org/2001/XMLSchema-instance"><addml:dataset/></addml:addml>"""
    tree_xml = ET.tostring(ET.fromstring(xml))
    assert tree == tree_xml


def test_iter_elements():
    """Test iter_elements"""
    file1 = f.definition_elems('flatFile', 'file1', reference='def1')
    file2 = f.definition_elems('flatFile', 'file2', reference='def2')
    file3 = f.definition_elems('flatFile', 'file3', reference='def3')
    xml = a.addml(child_elements=[file1, file2, file3])
    i = 0
    for ffile in a.iter_elements(xml, 'flatFile'):
        i = i + 1
        assert ffile.get('name') == 'file' + str(i)
    assert i == 3


def test_parse_name():
    """Test parse_name"""
    ffile = f.definition_elems('flatFile', 'filename1', reference='def1')
    assert a.parse_name(ffile) == 'filename1'


def test_parse_reference():
    """Test parse_reference"""
    ffile = f.definition_elems('flatFile', 'filename1', reference='def1')
    fdef = f.definition_elems('flatFileDefinition', 'def1', reference='type1')
    assert a.parse_reference(ffile) == 'def1'
    assert a.parse_reference(fdef) == 'type1'


def test_iter_sections():
    """Test iter_sections"""
    file1 = f.definition_elems('flatFile', 'file1', reference='def1')
    file2 = f.definition_elems('flatFile', 'file2', reference='def2')
    file3 = f.definition_elems('flatFile', 'file3', reference='def3')
    xml = a.addml(child_elements=[file1, file2, file3])
    i = 0
    for iter_elem in a.iter_sections(xml, 'flatFile'):
        i = i + 1
        assert iter_elem.get('name') == 'file' + str(i)
    assert i == 3


def test_sections_count():
    """Test sections_count"""
    file1 = f.definition_elems('flatFile', 'file1', reference='def1')
    file2 = f.definition_elems('flatFile', 'file2', reference='def2')
    file3 = f.definition_elems('flatFile', 'file3', reference='def3')
    xml = a.addml(child_elements=[file1, file2, file3])
    assert a.sections_count(xml, 'flatFile') == 3


def test_find_section_by_name():
    """Test find_section_by_name"""
    file1 = f.definition_elems('flatFile', 'file1', reference='def1')
    file2 = f.definition_elems('flatFile', 'file2', reference='def2')
    file3 = f.definition_elems('flatFile', 'file3', reference='def3')
    xml = a.addml(child_elements=[file1, file2, file3])

    ffile = a.find_section_by_name(xml, 'flatFile', 'file2')
    assert ffile.tag == '{http://www.arkivverket.no/standarder/addml}flatFile'
    assert ffile.get('definitionReference') == 'def2'


