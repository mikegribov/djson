
import os
from typing import Union
from pyparsing import ParseException
from .base_file import BaseFilePlugin
from .parser_xjson import ParserXJson


class PluginXJson(BaseFilePlugin):

    '''
    def __init__(self,  **kwargs):
        super().__init__(kwargs)
        self.parser = ParserXJson()
    '''

    def def_extensions(self) -> list:
        return {'xjson'}

    def load(self, content) -> Union[dict, list]:
        try:
            text = content.read()
            if text.strip() == '':
                result = {}
            else:
                self.parser = ParserXJson()
                self.parser.parse(text)
                result = self.parser.to_dict()

        except ParseException as ex:
            result = {'error': '{} file: {}'.format(ex, self.full_name)}
        return result
