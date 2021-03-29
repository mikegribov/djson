class DictReadonly(dict):

    def __setitem__(self, key, value):
        raise TypeError("'{}' object does not support item assignment".format(self.__class__.__name__))

    def __delitem__(self, key):
        raise TypeError("'{}' object does not support item deletion".format(self.__class__.__name__))

