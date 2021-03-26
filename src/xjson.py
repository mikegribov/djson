# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 00:22:32 2020

@author: Michael Gribov
"""

import os
import copy
from typing import Union, Any


try:
    import simplejson as json
except ImportError:
    import json

from .plugins.base_file import BaseFilePlugin, _info
from .exceptions.file_exceptions import FileNotFoundException
from .options import Options
from .xnodes import XNode, XDict, XList, create_xnode
from .classes.file_list import FileList
# plugins
from .plugins.plugin_json import PluginJson
from .plugins.plugin_xjson import PluginXJson
from .plugins.plugin_text import PluginText
from .plugins.plugin_yaml import PluginYaml
# /plugins

_index, _aliases, _required_plugins, default_exts \
    = 'index', '_aliases', {'PluginJson', 'PluginXJson', 'PluginText', 'PluginYaml'}, ['json', 'xjson']

class XJson:
    def __init__(self, name: str = '', **options) -> None:
        self._options = Options(options)
        self.structure = XDict(owner=self)                 # result structure
        self._load_plugins()
        self.file_list = FileList()
        if name > '':
            self._scan(name)

    def _load_plugins(self):
        self.plugins = {}
        list = _required_plugins
        try:
            list.update(set(self.options.plugins))
        except KeyError:
            pass

        for name in list:
            cl = globals().get(name, None)
            if cl is not None:
                self.plugins[name] = cl


    def _scan(self, name: str) -> None:
        ''' Scan the directory or file to form common structure'''
        file_name = name
        exts = [''] + ['.' + val for val in default_exts]

        for ext in exts:
            if os.path.exists(file_name + ext):
                self.structure = self._node_from_file(file_name + ext)
                break

    '''
    def _create_structure_by_dict(self, data: dict) -> XDict:
        result = XDict(owner=self)
        for name in data:
            value = data[name]
            result[name] = self.create_structure(value)
        return result

    def _create_structure_by_list(self, data: list) -> XList:
        result = XList(owner=self)
        for value in data:
            result.append(self.create_structure(value))
        return result

    def create_structure(self, data: XNode = None) -> XNode:

        if isinstance(data, dict):
            result = self._create_structure_by_dict(data)
        elif isinstance(data, list):
            result = self._create_structure_by_list(data)
        else:
            if data is None: data = {}
            result = data
        return result
    '''
    def _get_index_file(self, path):
        """find index file with extension priority from default_exts"""
        _fn = os.path.join(path, "index")
        for ext in default_exts:
            fn = _fn + "." + ext
            if os.path.exists(fn):
                return fn

    def _node_from_file(self, file_name: str) -> XNode:
        """Create nmode from file """
        file = self.file_list.get(file_name)
        if file.is_file:
            node = self._apply_plugins(file_name)
        else:
            index_fn = self._get_index_file(file_name)
            index_file = self.file_list.get(index_fn)
            if index_file is None:
                node = XDict(owner=self, _file=file)
            else:
                node = self._apply_plugins(index_fn)


            files = os.listdir(file_name)
            for fn in files:
                #if fn == _index.split(".")[:-1]:
                if index_file is not None and fn == index_file.name:
                    continue
                (name, ext) = os.path.splitext(fn)
                if name not in node:
                    node[name] = XDict(owner=self, _file=file)
                value = self._node_from_file(os.path.join(file_name, fn))
                if isinstance(value, XDict):
                    node[name].update(value)
                elif isinstance(value, XList):
                    node[name].append(value)
                else:
                    node[name] = value

        return node

    def _apply_plugins(self, file_name: str) -> XNode:
        '''Apply plugins to the file file_name and create & return node'''
        for name in  self.plugins:
            Plugin = self.plugins[name]
            plugin = Plugin(file_name)
            if plugin.check():
                return plugin.get()

        return XDict(self)

    def __str__(self):
        return self.dump()


    def clear(self):
        self.structure = {}

    def refresh(self, name = '') -> None:
        self.clear()
        self._scan(name)

    def alias(self, name: str):
        self.structure.alias(name)

    @property
    def options(self) -> Options:
        return self._options

    def _dump_val(self, node, key='', short=True, indent='', exclude_info=True):
        return "{}{}{}\n".format(indent, key + (": " if key else ""), node)

    def _dump_arr(self, node: XList, key='', short=True, indent='', exclude_info=True):
        result = ''
        n = 0
        for value in node:
            value = self.dump(value, key="#" + str(n), short=short, indent=indent + ". ", exclude_info=exclude_info)
            result += value
            n += 1

        result = '{0}{1}{2}'.format(indent, (key + ": \n" if key else ""), result)
        return result

    def _dump_obj(self, node: XDict, key='', short=True, indent='', exclude_info=True):
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

        if isinstance(node, XList):
            result = self._dump_arr(node, key=key, short=short, indent=indent)
        elif isinstance(node, XDict):
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
        self._options = src.options
        self._load_plugins()
        self.structure = src._copy_node(src.structure, False)
        return self

    def from_dict(self, data: dict):
        self.structure = copy.deepcopy(data)
        return self

    def to_dict(self, exclude_info = True):
        return self._copy_node(self.structure, exclude_info)
