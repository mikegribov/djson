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

DIRECTORY, FILE, _index, _size, _c_time, _type, _ext, _fn, _info = \
'directory', 'file', 'index', 'size', 'c_time', 'type', 'ext', 'fn', '_info'

class DJson:
    def _scan(self, name: str) -> None:
        ''' Scan the directory or file to form common structure'''
        file_name = name
        if not os.path.exists(file_name):
            file_name = file_name + '.json'
            if not os.path.exists(file_name):
                return
        self.structure = self._add_file(file_name)

    def _add_file(self, file_name: str) -> None:
        info = {
            _c_time: os.path.getctime(file_name),
            _fn: file_name,
        }

        if os.path.isfile(file_name):
            (name, ext) = os.path.splitext(file_name)
            file_size = os.path.getsize(file_name)
            node = self.get_json_file(file_name) if file_size else {}
            info.update({
                _size: file_size,
                _type: FILE,
                'name': name.split(os.sep)[-1],
                _ext: ext[1:]
            })
        else:
            index_fn = os.path.join(file_name, _index + '.json')
            node = self.get_json_file(index_fn) if os.path.exists(index_fn) else {}
            files = os.listdir(file_name)
            for fn in files:
                if fn == _index + '.json':
                    continue
                (name, ext) = os.path.splitext(fn)
                if name not in node:
                    node[name] = {}
                node[name].update(self._add_file(os.path.join(file_name, fn)))
            info.update({
                _type: DIRECTORY,
                'name': file_name.split(os.sep)[-1]
            })
        node.update({
            _info: info
        })

        return node

    def _add_dir(self, dir_name: str) -> None:
        index_fn = os.path.join(dir_name, _index + '.json')
        node = self.get_json_file(index_fn) if os.path.exists(index_fn) else {}
        files = os.listdir(dir_name)
        node.update({
            _info: {
                _c_time: os.path.getctime(dir_name),
                _type: DIRECTORY,
                _fn: dir_name,
                'name': dir_name.split(os.sep)[-1]
            }
        })

        return node

    @staticmethod
    def get_json_file(fn: str) -> dict:

        result = {}

        if os.path.isfile(fn):
            try:
                with open(fn, 'r', encoding='utf-8') as file:
                    result = json.load(file)
            except json.JSONDecodeError as ex:
                result = {'error': '{} file: {}'.format(ex, fn)}
        return result

    def __init__(self, name: str) -> None:
        self.base: str = name                    # base directory name
        self.structure = {}                 # result structure
        self._scan(self.base)


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

    def _copy_node(self, node: Union[dict, list] = None, exclude_info = False):
        result = {}
        for name in node:
            if exclude_info and name == _info:
                continue
            value = node[name]
            if isinstance(value, dict) or isinstance(value, list):
                value = self._copy_node(value, exclude_info)
            result[name] = value
        return result

    def copy(self, exclude_info = False):
        return self._copy_node(self.structure, exclude_info)
