import os
from typing import Union
from .base import BasePlugin
from ..exceptions.file_exceptions import FileNotFoundException, IsNotFileException
#from httplib2 import HTTPException


DIRECTORY, FILE, _size, _c_time, _type, _ext, _fn, _info = \
'directory', 'file', 'size', 'c_time', 'type', 'ext', 'fn', '_info'

F_ALL, F_FILE_NOT_FOUND, F_IS_NOT_FILE = 255, 1, 2

class BaseFilePlugin(BasePlugin):

    def _init(self,  **kwargs):
        name = self.full_name.split(os.sep)[-1]
        self.name, self.ext = os.path.splitext(name)
        self.ext = self.ext[1:]
        # self.file_size = os.path.getsize(self.full_name)
        self._extensions = set(self.def_extensions())
        if 'extensions' in kwargs:
            self._extensions.update(set(kwargs['extensions']))

    def def_extensions(self) -> set:
        return set()

    @property
    def extensions(self) -> set:
        return self._extensions

    def check(self) -> bool:
        return self.ext in self.extensions

    def load(self, content) -> Union[bool, str, int, float, list, dict]:
        pass

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

    def get(self) -> Union[bool, str, int, float, list, dict]:
        BaseFilePlugin.check_file(self.full_name)
        try:
            with open(self.full_name, 'r', encoding='utf-8') as file:
                result = self.load(file)
                #if isinstance(result, dict):
                #    result[_info] = BaseFilePlugin.get_file_info(self.full_name)
        except Exception as ex:
            result = {'error': '{} file: {}'.format(ex, self.full_name)}
        return result