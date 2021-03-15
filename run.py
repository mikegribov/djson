# -*- coding: utf-8 -*-

from src.djson import DJson
import os
import sys

from src.plugins.json import PluginJson

#plugin = PluginJson("D:\\WORK\\GITHUB\\djson\\tests\examples\\single_file_objarr.json")
#print(plugin.get())

#fj = FiledJson(os.path.join("examples", "countries"))

#dj = DJson(os.path.join("tests", "examples", "countries", "single_file"))
#dj = DJson(os.path.join("tests", "examples", "empty_file"))
#dj = DJson(os.path.join("examples", "single_file_object"))
#dj = DJson(os.path.join("examples", "empty_dir"))
dj = DJson(os.path.join("tests", "examples", "countries", "dir_several_level"))

print(dj.dump())

#print(dj.copy(exclude_info = True))
#print(dj.structure)
