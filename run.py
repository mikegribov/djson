# -*- coding: utf-8 -*-

from djson import Djson
import os


#fj = FiledJson(os.path.join("examples", "countries"))

dj = Djson(os.path.join("examples", "countries"))


print(dj)

print(dj.structure)
