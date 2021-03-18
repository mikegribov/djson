from djson.src.djson import DJson
import os


def get_result(name):
    dj = DJson(os.path.join("examples", name))
    return dj.structure

def test_single_file_object():
    result = get_result("single_file_object")
    assert result['name1'] == 'value1'
    assert result['name2'] == 'value2'
    assert result['name3'] == 'value3'
    info = result['_info']
    assert info['type'] == 'file'
    assert info['ext'] == 'json'
    assert info['name'] == 'single_file_object'
    assert info['size'] == 66

def test_single_file_objarr():
    result = get_result("single_file_objarr")
    assert result['name1'] == 'value1'
    assert result['name2'] == 'value2'
    assert result['name3'] == 'value3'
    assert result['arr'] == ["element1", "element2", "element3"]
    info = result['_info']
    assert info['type'] == 'file'
    assert info['ext'] == 'json'
    assert info['name'] == 'single_file_objarr'

def test_single_file_array():
    result = get_result("single_file_array")
    assert result == ["element1", "element2", "element3"]

def test_single_file_array():
    result = get_result("single_file_array")
    assert result == ["element1", "element2", "element3"]

def test_single_file_arrobj():
    result = get_result("single_file_arrobj")
    assert result == [{"name": "object1", "title": "Object one"}, {"name": "object1", "title": "Object two"},	{"name": "object3", "title": "Object three"}]