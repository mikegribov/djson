# -*- coding: utf-8 -*-

from src.xjson import XJson
from src.xnodes import XList
import os
import sys

from src.plugins.plugin_json import PluginJson

from src.classes.file_list import FileList
'''
import yaml
with open(os.path.join("tests", "examples", "countries", "single_file.yaml")) as file:
    document = file.read()
    try:
        print(yaml.safe_load(document))
    except yaml.parser.ParserError as ex:
        print(ex)
'''


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
xj = XJson(os.path.join("tests", "examples", "countries", "single_file.yaml"))
print(xj)
#print(xj.dump())

#print(xj.structure.alias('russia_population'))
#print(xj.structure['russia_population'])

#print(dj.get_value('russia.population'))
#print(xj.alias('russia_population'))

#print(XJson().copy_from(dj))
#print(dj.copy(exclude_info = True))
#print(dj.structure)
