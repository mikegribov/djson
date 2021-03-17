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


from .plugins.base_file import BaseFilePlugin, _info
from .plugins.json import PluginJson
from .exceptions.file_exceptions import FileNotFoundException

_index = 'index'

class DJson:
    def __init__(self, name: str, options: tuple = None) -> None:
        self._options = () if options is None else options
        self.structure = {}                 # result structure
        self._scan(name)

    def _scan(self, name: str) -> None:
        ''' Scan the directory or file to form common structure'''
        file_name = name
        if not os.path.exists(file_name):
            file_name = file_name + '.json'
            if not os.path.exists(file_name):
                return
        self.structure = self._add_file(file_name)

    def _add_file(self, file_name: str) -> None:


        if os.path.isfile(file_name):
            node = self._apply_plugins(file_name)
        else:
            index_fn = os.path.join(file_name, _index + '.json')
            try:
                node = self._apply_plugins(index_fn)
            except FileNotFoundException:
                node = {}

            info = node.get(_info, {})
            files = os.listdir(file_name)
            for fn in files:
                if fn == _index + '.json':
                    continue
                (name, ext) = os.path.splitext(fn)
                if name not in node:
                    node[name] = {}
                node[name].update(self._add_file(os.path.join(file_name, fn)))

            info.update(BaseFilePlugin.get_file_info(file_name))
            node[_info] = info

        return node

    def _apply_plugins(self, file_name: str) -> dict:
        '''Apply plugins to the file file_name '''
        plugin = PluginJson(file_name)
        return  plugin.get()


    def __str__(self):
        return self.dump()

    @property
    def options(self) -> tuple:
        return self.options

    def dump(self, node: Union[dict, list] = None, short=True, indent=''):
        result = ''
        if node is None:
            node = self.structure

        for name in node:
            if not short or name[:1] != '_' and name != 'name':
                value = node[name]
                if not short or value is not None:
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
