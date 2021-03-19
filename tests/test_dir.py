from xjson.src.xjson import XJson
import os

def check(name):
    xj0 = XJson(os.path.join("examples", "countries", "single_file"))
    xj = XJson(os.path.join("examples", "countries", name))
    assert xj0.to_dict(exclude_info = True) == xj.to_dict(exclude_info = True)

def test_dir_one_level():
    check("dir_one_level")

def test_dir_several_level():
    check("dir_several_level")
