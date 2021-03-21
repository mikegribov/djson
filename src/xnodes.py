from typing import Any

_aliases = '_aliases'


class XNode(dict):
    __slots__ = '_aliases', '_owner', '_src'
    _aliases: dict
    _src: dict
    _owner: Any

    def __init__(self, owner=None, **kwargs):
        super().__init__(**kwargs)
        self._owner = owner
        self._aliases = {}

    def __setitem__(self, key, value):
        """ to hook _alias key setting"""
        if key == _aliases:
            self._aliases = value
        else:
            super().__setitem__(key, value)

    def __getitem__(self, key):
        """ to hook getting by key for check aliases. key name has more priority than alias name"""
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

########################################################################################################################


class XDict(XNode):
    pass


########################################################################################################################

class XList(XNode):
    """ List Node for xjson structure """
    def __init__(self, owner=None, *args):
        super().__init__(owner)
        self.append(*args)

    def __iter__(self):
        return iter(self.values())

    def __getitem__(self, key):
        print("key: ", key)
        if isinstance(key, int) or (key in self._aliases):
            result = super().__getitem__(key)
        else:
            raise TypeError('list indices must be integers or slices, not str')
        return result

    def __setitem__(self, key, value):
        """ to hook _alias key setting"""
        if isinstance(key, int) or key == _aliases:
            result = super().__setitem__(key, value)
        else:
            raise TypeError('list indices must be integers or slices, not str')

    def __str__(self):
        return list(self.__iter__()).__str__()

    def append(self, *args):
        """ Append object to the end of the list. Emulate list.append(...)"""
        i = len(self)
        for value in args:
            self[i] = value
            i += 1
