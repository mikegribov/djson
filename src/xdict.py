from typing import List, Union, Any

_aliases = '_aliases'

class XDict(dict):
    __slots__ = '_aliases', '_owner'
    _aliases: dict
    _owner: Any

    def __init__(self, owner=None, **kwargs):
        super().__init__(**kwargs)
        self._owner = owner
        self._aliases = {}

    def __setitem__(self, key, value):
        ''' to hook _alias key setting'''
        if key == _aliases:
            self._aliases = value
        else:
            super().__setitem__(key, value)


    def __getitem__(self, key):
        ''' to hook getting by key for check aliases. key name has more prority than alias name'''
        try:
            result = super().__getitem__(key)
        except KeyError as ex:
            result = self.alias(key)
            if result is None:
                raise ex
        return result

    def _get_value(self, path: list, node: Any = None):
        if node is None:
            node = self
        if not len(path):
            return node
        name = path[0]
        if isinstance(node, XDict):
            if name in node:
                return self._get_value(path[1:], node[name])
        elif isinstance(node, list):
            i = int(name)
            if 0 <= i < len(node):
                return self._get_value(path[1:], node[i])
        return None

    def get_value(self, path: str):
        return self._get_value(path.split('.'))

    def alias(self, name: str):
        try:
            path = self._aliases[name]['ref']
            return self.get_value(path)
        except IndexError:
            pass

    @property
    def owner(self):
        return self._owner