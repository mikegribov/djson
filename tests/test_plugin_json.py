import os
from ..xjson.plugins.plugin_json import PluginJson
from ..xjson.exceptions.file_exceptions import FileNotFoundException, IsNotFileException
from ..xjson.xnodes import create_xnode

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
    assert res == create_xnode(None, result)

def test_not_exists():
    hasException = False
    #check("not_eixsts1", {})

    try:
        check("not_eixsts", {})
    except FileNotFoundException:
        hasException = True
    
    assert hasException == True



def test_object():
    check("obj", {'name1': 'value1', 'name2': 'value2', 'name3': 'value3'})

def test_array():
    check("arr", ['element1', 'element2', 'element3'])

def test_arrayobj():
    check("arr_obj", [{"name": "object1", "title": "Object one"}, {"name": "object1", "title": "Object two"},	{"name": "object3", "title": "Object three"}])

def test_objarr():
    check("obj_arr", {'name1': 'value1', 'name2': 'value2', 'name3': 'value3', 'arr': ['element1', 'element2', 'element3']})
