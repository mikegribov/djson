# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 00:22:32 2020

@author: Michael Gribov
"""

import os
from typing import List, Union
try:
    import simplejson as json
except ImportError:
    import json


DIRECTORY = 'directory'
FILE = 'file'
_size = '_size'
_c_time = '_c_time'
_type = '_type'
_ext = '_ext'
_fn = '_fn'
_info = '_info'


class DJson:

    def _scan(self, directory: str) -> None:
        file_name = directory + '.json'
        if os.path.isfile(file_name) and os.path.exists(file_name):
            self._add_file(file_name, True)
            print(self.structure)
        else:

            for dir_path, dir_names, file_names in os.walk(directory):

                for dir_name in dir_names:
                    self._add_dir(dir_name)
                for file_name in file_names:
                    self._add_file(file_name)

            self.structure[self.name] = self.structure.pop('')

    def _full_file_name(self, name: str) -> str:
        return os.path.join(self.base, self.dir.lstrip('\\'), name)

    def _add_file(self, file_name: str, full_name=False) -> None:

        if full_name:
            fn = file_name
            file_name = os.path.split(file_name)[1]
        else:
            fn = self._full_file_name(file_name)

        (name, ext) = os.path.splitext(file_name)

        if name == _info:
            return

        node = self.get_json_file(fn)

        if name in self.current:
            node = node.update(self.current[name])

        node.update({
            _c_time: os.path.getctime(fn),
            _size: os.path.getsize(fn),
            _type: FILE,
            _ext: ext[1:],
            _fn: fn,
            'name': name
        })

        self.current[name] = node

    def _add_dir(self, dir_name: str) -> None:

        fn = self._full_file_name(dir_name)
        name = dir_name

        node = self.get_json_file(fn + os.sep + _info + '.json')

        if name in self.current:
            node = node.update(self.current[name])

        node.update({
            _c_time: os.path.getctime(fn),
            _type: DIRECTORY,
            _fn: fn,
            'name': name
        })

        self.current[name] = node

    @staticmethod
    def get_json_file(fn: str) -> dict:

        result = {}

        if os.path.isfile(fn):
            try:
                with open(fn, 'r', encoding='utf-8') as file:
                    result = json.load(file)
            except json.JSONDecodeError as ex:
                result = {'error': ex}
        return result

    def __init__(self, name: str) -> None:
        self.base: str = name                    # base directory name
        self.name: str = os.path.split(name)[1]  # name of root node
        self.dir = ''                       # current directory related base directory
        self.structure = {}                 # result structure
        self.current = self.structure       # current structure node
        self._scan(self.base)

    def set_current(self, path: List[str]) -> dict:
        if len(path) and path[0] != '':
            path.insert(0, '')

        self.current = self.structure
        p = []
        for name in path:
            p.append(name)
            if not (name in self.current):
                self._add_dir(name)

            self.dir = os.sep.join(p)
            self.current = self.current[name]

        return self.current

    def __str__(self):
        return self.dump()

    def dump(self, node: Union[dict, list] = None, short=True, indent=''):
        result = ''
        if node is None:
            node = self.structure

        for name in node:
            if not short or name[:1] != '_' and name != 'name':
                value = node[name]
                if not short or value:
                    if not (isinstance(value, dict) or isinstance(value, list)):
                        result += "{}{}: {}\n".format(indent, name, value)

        for name in node:
            value = node[name]
            if isinstance(value, dict) or isinstance(value, list):
                result += "{}{}:\n" .format(indent, name)
                result += self.dump(value, short, indent + ". ")
        return result
