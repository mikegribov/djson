try:
    import simplejson as json
except ImportError:
    import json
from typing import Any
from .base_file import BaseFilePlugin
from ..xnodes import create_xnode, XNode, XDict, XFileError
from ..classes.file_list import FileList


class PluginText(BaseFilePlugin):

    def def_extensions(self) -> set:
        return {'txt'}

    def load(self, content) -> XNode:
        if content.strip() == '':
            result = XDict(_file=self.file)
        else:
            result = create_xnode(None, content, _file=self.file)

        return result

