import os
import traceback
from ..xjson import XJson


def check_same_structure(name, ext):
    json = XJson(os.path.join("examples", "single_file_" + name + ".json"))
    plugin = XJson(os.path.join("examples", "single_file_" + name + "." + ext))
    assert json.structure != {} and json.structure == plugin.structure

def check_same_structure_by_stack():
    stack = traceback.extract_stack()
    name = stack[-2][2]
    args = name.split('_')
    check_same_structure("_".join(args[2:]), args[1])


def test_xjson_arr():
    check_same_structure_by_stack()

def test_xjson_arr_arr():
    check_same_structure_by_stack()

def test_xjson_arr_obj():
    check_same_structure_by_stack()

def test_xjson_obj():
    check_same_structure_by_stack()

def test_xjson_obj_arr():
    check_same_structure_by_stack()

def test_xjson_obj_obj():
    check_same_structure_by_stack()


def test_yaml_arr():
    check_same_structure_by_stack()

def test_yaml_arr_arr():
    check_same_structure_by_stack()

def test_yaml_arr_obj():
    check_same_structure_by_stack()

def test_yaml_obj():
    check_same_structure_by_stack()

def test_yaml_obj_arr():
    check_same_structure_by_stack()

def test_yaml_obj_obj():
    check_same_structure_by_stack()


def test_xml_arr():
    check_same_structure_by_stack()

def test_xml_arr_arr():
    check_same_structure_by_stack()

def test_xml_arr_obj():
    check_same_structure_by_stack()

def test_xml_obj():
    check_same_structure_by_stack()

def test_xml_obj_arr():
    check_same_structure_by_stack()

def test_xml_obj_obj():
    check_same_structure_by_stack()