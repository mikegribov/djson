try:
    import simplejson as json
except ImportError:
    import json
from typing import Union
from .base_file import BaseFilePlugin


class PluginJson(BaseFilePlugin):

    def def_extensions(self) -> list:
        return {'json'}

    def load(self, content) -> Union[dict, list]:
        try:
            text = content.read()
            if text.strip() == '':
                result = {}
            else:
                result = json.loads(text)
        except json.JSONDecodeError as ex:
            result = {'error': '{} file: {}'.format(ex, self.full_name)}
        return result
