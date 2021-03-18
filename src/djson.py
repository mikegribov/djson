# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 00:22:32 2020

@author: Michael Gribov
"""

import os
import copy
from typing import List, Union

try:
    import simplejson as json
except ImportError:
    import json


from .plugins.base_file import BaseFilePlugin, _info
from .plugins.json import *
from .exceptions.file_exceptions import FileNotFoundException
from .classes.dict_readonly import DictReadonly

_index = 'index'
_default_plugins = {'PluginJson'}
class DJson:
    def __init__(self, name: str = '', **options) -> None:
        self._options = DictReadonly(options)
        self.structure = {}                 # result structure
        self._load_plugins()
        if name > '':
            self._scan(name)

    def _load_plugins(self):
        self.plugins = {}
        list = _default_plugins
        try:
            list.update(set(self.options["plugins"]))
        except KeyError:
            pass

        for name in list:
            cl = globals().get(name, None)
            if cl is not None:
                self.plugins[name] = cl


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
        for name in  self.plugins:
            Plugin = self.plugins[name]
            return  Plugin(file_name).get()


    def __str__(self):
        return self.dump()

    def clear(self):
        self.structure = {}

    def refresh(self, name = '') -> None:
        self.clear()
        self._scan(name)

    @property
    def options(self) -> DictReadonly:
        return self._options

    def _dump_val(self, node, key='', short=True, indent='', exclude_info=True):
        return "{}{}{}\n".format(indent, key + (": " if key else ""), node)

    def _dump_arr(self, node: list, key='', short=True, indent='', exclude_info=True):
        result = ''
        n = 0
        for value in node:
            value = self.dump(value, key="#" + str(n), short=short, indent=indent + ". ", exclude_info=exclude_info)
            result += value
            n += 1

        result = '{0}{1}{2}'.format(indent, (key + ": \n" if key else ""), result)
        return result

    def _dump_obj(self, node: dict, key='', short=True, indent='', exclude_info=True):
        result = ''

        for name in node:
            if exclude_info and name == _info:
                continue
            value = node[name]
            value = self.dump(value, key=name, short=short, indent=indent + ". ", exclude_info=exclude_info)
            result += value
        result = '{}{}{}'.format(indent, (key + ": \n" if key else ""), result)
        return result

    def dump(self, node=None, key='', short=True, indent='', exclude_info = True):
        result = ''
        if node is None:
            node = self.structure

        if isinstance(node, list):
            result = self._dump_arr(node, key=key, short=short, indent=indent)
        elif isinstance(node, dict):
            result = self._dump_obj(node, key=key, short=short, indent=indent)
        else:
            result = self._dump_val(node, key=key, short=short, indent=indent)

        return result

    def _copy_node(self, node: Union[dict, list] = None, exclude_info = False):

        if isinstance(node, dict): # for DICT
            result = {}
            for name in node:
                if exclude_info and name == _info:
                    continue
                value = node[name]
                if isinstance(value, dict) or isinstance(value, list):
                    value = self._copy_node(value, exclude_info)
                result[name] = value
        else: # for LIST
            result = []
            for value in node:
                if isinstance(value, dict) or isinstance(value, list):
                    value = self._copy_node(value, exclude_info)
                result.append(value)
        return result


    def copy_from(self, src):
        self.structure = src._copy_node(src.structure, False)
        return self

    def from_dict(self, data: dict):
        self.structure = copy.deepcopy(data)
        return self

    def to_dict(self, exclude_info = True):
        return self._copy_node(self.structure, exclude_info)
