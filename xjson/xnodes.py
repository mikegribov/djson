from typing import Union, Any
from .file_list import FileList, FileInfo

_aliases = '_aliases'


class XNode(dict):
    __slots__ = '_aliases', '_owner', '_src', '_file'
    _aliases: dict
    _src: dict
    _owner: Any
    _file: Union[None, FileInfo]

    def __init__(self, owner:Any=None, **kwargs):
        super().__init__(**kwargs)
        self._owner = owner
        self._aliases = {}
        self._file = None
        if '_file' in kwargs:
            self._file = kwargs["_file"]
            del self['_file']
        elif '_file_name' in kwargs:
            file_name = kwargs["_file_name"]
            self._file = FileList().get(file_name=file_name)
            del self['_file_name']

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

    @property
    def file(self):
        return self._file

########################################################################################################################


class XDict(XNode):
    pass


########################################################################################################################

class XList(XNode):
    """ List Node for xjson structure """
    def __init__(self, owner:Any=None, *args, **kwargs):
        super().__init__(owner, **kwargs)
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

    def from_list(self, *args) -> None:
        """ fill bby data from list or args """
        if len(args) == 1 and isinstance(args, list):
            self.append(args[0])
        else:
            self.append(args)

    def append(self, *args) -> None:
        """ Append object to the end of the list. Emulate list.append(...)"""
        i = len(self)
        for value in args:
            self[i] = value
            i += 1

########################################################################################################################

class XError(XNode):
    pass

########################################################################################################################

class XFileError(XError):
    def __str__(self):
        return 'Error {} file: {}'.format(self.get("name", ""), self._file.full_name)


########################################################################################################################
def create_xnode(owner:Any=None, data: Any=None, **kwargs) -> Any:
    if isinstance(data, list):
        result = XList(owner, **kwargs)
        for item in data:
            result.append(create_xnode(owner, item, **kwargs))
    elif isinstance(data, dict):
        result = XDict(owner, **kwargs)
        for name in data:
            result[name] = create_xnode(owner, data[name], **kwargs)
    else:
        result = data
    return result