from typing import List, Union

class Options:
    _frozen: bool = False
    plugins: set

    def __init__ (self, plugins: Union[set, list]):
        self.plugins = set(plugins)
        self._frozen = True

    def __setattr__(self, key, value):
        if self._frozen:
            raise TypeError("'{}' object does not support item assignment".format(self.__class__.__name__))
        else:
            super().__setattr__(key, value)

    def __delattr__(self, key):
        if self._frozen:
            raise TypeError("'{}' object does not support item deletion".format(self.__class__.__name__))
        else:
            super().__delattr__(key)
