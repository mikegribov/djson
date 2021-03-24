import os
from typing import Any, Union
from .base import BasePlugin
from ..exceptions.file_exceptions import FileNotFoundException, IsNotFileException
from ..classes.file_list import  FileList, F_FILE_NOT_FOUND
from ..xnodes import XNode
from ..classes.file_list import FileList
#from httplib2 import HTTPException


DIRECTORY, FILE, _size, _c_time, _type, _ext, _fn, _info = \
'directory', 'file', 'size', 'c_time', 'type', 'ext', 'fn', '_info'


class BaseFilePlugin(BasePlugin):

    def _init(self,  **kwargs):
        self._extensions = set(self.def_extensions())
        if 'extensions' in kwargs:
            self._extensions.update(set(kwargs['extensions']))

        self.file = FileList().get(self.full_name)

    def def_extensions(self) -> set:
        return set()

    @property
    def extensions(self) -> set:
        return self._extensions

    def check(self) -> bool:
        return self.file.ext in self.extensions

    def load(self, content) -> XNode:
        pass

    '''
    @staticmethod
    def check_file(file_name, flags = F_ALL):
        if (F_FILE_NOT_FOUND & flags) and not os.path.exists(file_name):
            raise (FileNotFoundException(file_name))
        if (F_IS_NOT_FILE & flags) and not os.path.isfile(file_name):
            raise (IsNotFileException(file_name))

    @staticmethod
    def get_file_info(file_name):
        BaseFilePlugin.check_file(file_name, F_FILE_NOT_FOUND)
        result = {
            _c_time: os.path.getctime(file_name),
            _fn: file_name,
        }
        if os.path.isfile(file_name):
            (name, ext) = os.path.splitext(file_name)
            file_size = os.path.getsize(file_name)

            result.update({
                _size: file_size,
                _type: FILE,
                'name': name.split(os.sep)[-1],
                _ext: ext[1:]
            })
        else:
            result.update({
                _type: DIRECTORY,
                'name': file_name.split(os.sep)[-1]
            })
        return result
    '''
    def get(self) -> XNode:
        self.file.check(F_FILE_NOT_FOUND)
        return self.load(self.file.content)