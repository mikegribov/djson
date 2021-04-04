import os
from ..xjson import XJson
from ..xjson.file_list import FileList

def test_text_value():

    xjson = XJson(os.path.join("examples", "several_file_types"))
    value_from_xjson = xjson.structure['text']
    text_file = FileList().get(os.path.join("examples", "several_file_types", "text.txt"))
    assert value_from_xjson == text_file.content