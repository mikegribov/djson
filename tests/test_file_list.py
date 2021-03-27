from xjson.src.classes.file_list import FileList, F_FILE_NOT_FOUND
import os
from xjson.src.exceptions.file_exceptions import FileNotFoundException, IsNotFileException



def test_file_caching():
    file_list = FileList()
    file_list.clear()
    fn = os.path.join("examples", "single_file_obj.json")
    file_list.get(fn)
    file_list.get(fn)
    file_list.get(fn, True)

    l = file_list._list
    assert len(l) == 1
    assert list(l.keys())[0] == fn


def test_file_info():
    file_list = FileList()
    file_list.clear()
    fn = os.path.join("examples", "single_file_obj.json")
    file_list.get(fn)
    l = file_list._list
    info = l.get(fn)
    assert info.full_name == fn
    assert info.c_time == os.path.getctime(fn)
    assert info.size == os.path.getsize(fn)
    assert info.name == "single_file_obj.json"
    assert info.ext == "json"
    assert info.is_file == True
    assert info.is_directory == False

def test_dir_info():
    file_list = FileList()
    file_list.clear()
    fn = os.path.join("examples", "countries", "dir_one_level")
    file_list.get(fn)
    l = file_list._list
    info = l.get(fn)
    assert info.full_name == fn
    assert info.c_time == os.path.getctime(fn)
    assert info.size == 0
    assert info.name == "dir_one_level"
    assert info.ext == ""
    assert info.is_file == False
    assert info.is_directory == True

def test_singleton():
    fn = os.path.join("examples", "countries", "dir_one_level")
    file_list1 = FileList()
    file_list1.clear()
    file_list1.get(fn)
    file_list = FileList()
    file_list.clear()
    file_list.get(fn)
    l = file_list._list
    info = l.get(fn)
    assert info.full_name == fn


def test_checking():
    file_list = FileList()
    file_list.clear()
    file = file_list.get(os.path.join("examples", "not_exists"), False)
    try:
        file.check()
        res = True
    except FileNotFoundException:
        res = False

    assert res == False

    file = file_list.get(os.path.join("examples", "countries", "dir_one_level"), False)
    try:
        file.check()
        res = True
    except IsNotFileException:
        res = False

    assert res == False

    file = file_list.get(os.path.join("examples", "countries", "dir_one_level"), False)
    try:
        file.check(F_FILE_NOT_FOUND)
        res = True
    except IsNotFileException:
        res = False

    assert res == True