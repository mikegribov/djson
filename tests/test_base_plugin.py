from djson.src.plugins.base import BaseFilePlugin
import os

def test_extensions():
    extensions = {'ext1', 'ext2', 'ext3'}
    plugin0 = BaseFilePlugin('')
    plugin = BaseFilePlugin('', extensions=extensions)
    assert plugin.extensions == plugin0.extensions.union(extensions)

