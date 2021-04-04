from pyparsing import ParseException
from .base_file import BaseFilePlugin
from .parser_xjson import ParserXJson
from ..xnodes import create_xnode, XNode, XDict, XFileError
from ..file_list import FileList

class PluginXJson(BaseFilePlugin):

    def def_extensions(self) -> set:
        return {'xjson'}

    def load(self, content) -> XNode:
        file = FileList().get(self.full_name)

        if content.strip() == '':
            result = XDict(_file=file)
        else:
            try:
                self.parser = ParserXJson()
                self.parser.parse(content)
                result = create_xnode(None, self.parser.to_dict(), _file=file)
            except ParseException as ex:
                result = XFileError(name=ex, _file=file)
        return result
