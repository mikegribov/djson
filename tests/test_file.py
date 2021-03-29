from ..xjson import XJson
import os


def get_result(name):
    xj = XJson(os.path.join("examples", name))
    return xj.structure

def test_single_file_object():
    result = get_result("single_file_obj")
    assert result['name1'] == 'value1'
    assert result['name2'] == 'value2'
    assert result['name3'] == 'value3'

def test_single_file_objarr():
    result = get_result("single_file_obj_arr")
    assert result['name1'] == 'value1'
    assert result['name2'] == 'value2'
    assert result['name3'] == 'value3'
    assert list(result['arr']) == ["element1", "element2", "element3"]

def test_single_file_array():
    result = get_result("single_file_arr")
    assert list(result) == ["element1", "element2", "element3"]

def test_single_file_arrobj():
    result = get_result("single_file_arr_obj")
    assert list(result) == [{"name": "object1", "title": "Object one"}, {"name": "object1", "title": "Object two"},	{"name": "object3", "title": "Object three"}]