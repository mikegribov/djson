import os
from typing import Union
from .base import BasePlugin
from ..exceptions.file_exceptions import FileNotFoundException, IsNotFileException

DIRECTORY, FILE, _size, _c_time, _type, _ext, _fn, _info = \
'directory', 'file', 'size', 'c_time', 'type', 'ext', 'fn', '_info'

class BaseFilePlugin(BasePlugin):

    def _init(self,  **kwargs):
        self._check_file()
        name = self.full_name.split(os.sep)[-1]
        self.name, self.ext = os.path.splitext(name)
        self.ext = self.ext[1:]
        # self.file_size = os.path.getsize(self.full_name)
        self._extensions = set(self.def_extensions())
        if 'extensions' in kwargs:
            self._extensions.update(set(kwargs['extensions']))

    def _check_file(self):
        if not os.path.exists(self.full_name):
            raise (FileNotFoundException(self.full_name))
        if not os.path.isfile(self.full_name):
            raise (IsNotFileException(self.full_name))

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
    def get_file_info(file_name):
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
        self._check_file()
        try:
            with open(self.full_name, 'r', encoding='utf-8') as file:
                result = self.load(file)
                result[_info] = BaseFilePlugin.get_file_info(self.full_name)
        except Exception as ex:
            result = {'error': '{} file: {}'.format(ex, self.full_name)}
        return result