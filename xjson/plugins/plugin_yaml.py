
from .base_file import BaseFilePlugin
from ..xnodes import create_xnode, XNode, XDict, XFileError
import yaml

class PluginYaml(BaseFilePlugin):

    def def_extensions(self) -> set:
        return {'yaml'}

    def load(self, content) -> XNode:

        if content.strip() == '':
            result = XDict(_file=self.file)
        else:
            try:
                result = create_xnode(None, yaml.safe_load(content), _file=self.file)
            except yaml.parser.ParserError as ex:
                result = XFileError(name=ex, _file=self.file)
        return result

