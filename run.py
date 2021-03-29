# -*- coding: utf-8 -*-

from xjson import XJson
from xjson.xnodes import XList
import os
import io
import sys
import traceback

from xjson.plugins.plugin_json import PluginJson
from xjson.classes.file_list import FileList
name, ext="arr", "xml"
plugin = XJson(os.path.join("tests", "examples", "single_file_" + name + "." + ext))
print(plugin.structure)

#plugin = PluginJson("D:\\WORK\\GITHUB\\xjson\\tests\examples\\single_file_objarr.json")
#print(plugin.get())

# fj = FiledJson(os.path.join("examples", "countries"))

#xj = XJson(os.path.join("tests", "examples", "countries", "single_file"))
#xj = XJson(os.path.join("tests", "examples", "empty_file"))
#xj = XJson(os.path.join("tests", "examples", "single_file_object.json"))
#xj = XJson(os.path.join("tests", "examples", "single_file_objarr.json"))
#xj = XJson(os.path.join("tests", "examples", "single_file_arrobj.json"))
#xj = XJson(os.path.join("tests", "examples", "single_file_array.json"))
#xj = XJson(os.path.join("tests", "examples", "several_file_types"))
#xj = XJson(os.path.join("tests", "examples", "empty_dir"))
#xj = XJson(os.path.join("tests", "examples", "countries", "dir_one_level"))
#xj = XJson(os.path.join("tests", "examples", "countries", "dir_several_level"))
#xj = XJson(os.path.join("tests", "examples", "countries", "single_file.xjson"))
#xj = XJson(os.path.join("tests", "examples", "countries", "single_file.yaml"))
#xj = XJson(os.path.join("tests", "examples", "countries", "single_file.csv"))
#xj = XJson(os.path.join("tests", "examples", "countries", "single_file.xml"))
#print(xj)

#print(xj.structure.alias('russia_population'))
#print(xj.structure['russia_population'])

#print(dj.get_value('russia.population'))
#print(xj.alias('russia_population'))

#print(XJson().copy_from(dj))
#print(dj.copy(exclude_info = True))
#print(dj.structure)
