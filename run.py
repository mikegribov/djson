# -*- coding: utf-8 -*-

from filedjson import FiledJson
import os


#fj = FiledJson(os.path.join("examples", "countries"))

fj = FiledJson(os.path.join("examples", "countries"))



print(fj)

print (fj.structure)

