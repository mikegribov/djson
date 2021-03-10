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