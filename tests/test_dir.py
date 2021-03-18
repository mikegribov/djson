from djson.src.djson import DJson
import os

def check(name):
    dj0 = DJson(os.path.join("examples", "countries", "single_file"))
    dj = DJson(os.path.join("examples", "countries", name))
    assert dj0.to_dict(exclude_info = True) == dj.to_dict(exclude_info = True)

def test_dir_one_level():
    check("dir_one_level")

def test_dir_several_level():
    check("dir_several_level")
