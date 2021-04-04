from ..xjson import XJson
import os


def check(name, value):
    xj = XJson(os.path.join("examples", name))
    assert xj.dump(xj.structure) == value

def test_empty_file():
    check("empty_file", '')

def test_single_file_obj():
    check("single_file_obj",". name1: value1\n. name2: value2\n. name3: value3\n")

def test_single_file_obj_arr():
    check("single_file_obj_arr", ". name1: value1\n. name2: value2\n. name3: value3\n. arr: \n. . #0: element1\n. . #1: element2\n. . #2: element3\n")

def test_single_file_arr():
    check("single_file_arr", ". #0: element1\n. #1: element2\n. #2: element3\n")

def test_single_file_arr_obj():
    check("single_file_arr_obj", ". #0: \n. . name: object1\n. . title: Object one\n. #1: \n. . name: object1\n. . title: Object two\n. #2: \n. . name: object3\n. . title: Object three\n")