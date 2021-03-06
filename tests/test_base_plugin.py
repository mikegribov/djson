from ..xjson.exceptions.file_exceptions import FileNotFoundException
from ..xjson.plugins.base_file import BaseFilePlugin
import os

def test_extensions():
    extensions = {'ext1', 'ext2', 'ext3'}
    try:
        plugin0 = BaseFilePlugin('')
    except FileNotFoundException:
        pass

    try:
        plugin = BaseFilePlugin('', extensions=extensions)
    except FileNotFoundException:
        pass

    assert plugin.extensions == plugin0.extensions.union(extensions)

