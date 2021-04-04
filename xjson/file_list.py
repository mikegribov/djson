import datetime
from typing import Any
import os
from .exceptions.file_exceptions import FileNotFoundException, IsNotFileException

F_ALL, F_FILE_NOT_FOUND, F_IS_NOT_FILE = 255, 1, 2

class FileInfo:
    full_name: str = ''
    name: str = ''
    ext: str = ''
    c_time: Any = None
    is_directory: bool = True
    size: int = 0
    content: str = ''
    exists: bool = False

    def __init__(self, file_name, load = True, load_content = True):
        self.full_name = file_name
        if load:
            self.load(file_name, load_content)

    def __str__(self):
        return "{}: '{}'".format("FILE" if self.is_file else "DIRECTORY", self.full_name)

    @property
    def is_file(self):
        return not self.is_directory

    def check(self, flags: int = F_ALL):
        if (F_FILE_NOT_FOUND & flags) and not os.path.exists(self.full_name):
            raise (FileNotFoundException(self.full_name))
        if (F_IS_NOT_FILE & flags) and not os.path.isfile(self.full_name):
            raise (IsNotFileException(self.full_name))

    def load(self, file_name, load_content = True):
        if os.path.exists(file_name):
            name = file_name.split(os.sep)[-1]
            (name, ext) = os.path.splitext(name)
            name = name + (ext if ext > '' else '')
            ext = ext[1:]
            self.full_name = file_name
            self.c_time = os.path.getctime(file_name)
            self.name = name
            self.ext = ext
            if os.path.isfile(file_name):
                self.is_directory = False
                self.size = os.path.getsize(file_name)

        if self.is_file and load_content:
            with open(self.full_name, 'r', encoding='utf-8') as file:
                self.content = file.read()


class FileList:
    """ Singleton """
    _instance = None
    _list: dict = {}

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            instance = super().__new__(cls)
        else:
            instance = cls._instance
        return instance

    def __init__(self):
        super().__init__()
        if self.__class__._instance is None:
            self.__class__._instance = self

    def clear(self):
        self._list.clear()

    def get(self, file_name, reload = False) -> FileInfo:
        if file_name is None:
            return None
        if file_name in self._list or reload:
            result = self._list[file_name]
        else:
            result = FileInfo(file_name)
            self._list[file_name] = result

        return result

