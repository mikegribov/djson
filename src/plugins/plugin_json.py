try:
    import simplejson as json
except ImportError:
    import json
from .base_file import BaseFilePlugin
from ..xnodes import create_xnode, XNode, XDict, XFileError


class PluginJson(BaseFilePlugin):

    def def_extensions(self) -> set:
        return {'json'}

    def load(self, content) -> XNode:
        #elf.full_name)
        if content.strip() == '':
            result = XDict(_file=self.file)
        else:
            try:
                result = create_xnode(None, json.loads(content), _file=self.file)
            except json.JSONDecodeError as ex:
                result = XFileError(name=ex, _file=self.file)
        return result
