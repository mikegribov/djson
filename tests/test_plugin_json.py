from xjson.src.plugins.plugin_json import PluginJson
import os
import pytest
from xjson.src.exceptions.file_exceptions import FileNotFoundException, IsNotFileException

def test_extensions():
    extensions = {'ext1', 'ext2', 'ext3'}
    plugin0 = PluginJson('')
    plugin = PluginJson('', extensions=extensions)
    assert plugin.extensions == plugin0.extensions.union(extensions)

def test_check():
    files = {"empty_file.json": True, "empty_file.ext.json": True, "empty_file.cfg": False}
    for name in files:
        plugin = PluginJson(os.path.join("examples", name))
        assert plugin.check() == files[name]

def check(name, result):
    plugin = PluginJson(os.path.join("examples", "single_file_" + name + ".json"))
    res = plugin.get()
    if '_info' in res:
        del res['_info']
    assert res == result

def test_not_exists():
    hasException = False
    #check("not_eixsts1", {})

    try:
        check("not_eixsts", {})
    except FileNotFoundException:
        hasException = True
    
    assert hasException == True



def test_object():
    check("object", {'name1': 'value1', 'name2': 'value2', 'name3': 'value3'})

def test_array():
    check("array", ['element1', 'element2', 'element3'])

def test_arrayobj():
    check("arrobj", [{"name": "object1", "title": "Object one"}, {"name": "object1", "title": "Object two"},	{"name": "object3", "title": "Object three"}])

def test_objarr():
    check("objarr", {'name1': 'value1', 'name2': 'value2', 'name3': 'value3', 'arr': ['element1', 'element2', 'element3']})

