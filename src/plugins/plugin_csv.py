from .base_file import BaseFilePlugin
from ..xnodes import create_xnode, XNode, XDict, XFileError
import io
import csv

_name = 'name'
class PluginCsv(BaseFilePlugin):

    def def_extensions(self) -> set:
        return {'csv'}

    def load(self, content) -> XNode:
        if content.strip() == '':
            result = XDict(_file=self.file)
        else:
            f = io.StringIO(content)
            reader = csv.DictReader(f)
            headers = reader.fieldnames
            is_dict = _name in headers
            rows = {} if is_dict else []
            for row in reader:
                if is_dict:
                    n = row[_name]
                    del row[_name]
                    rows[n] = row

                else:
                    rows.append(row)
            result = create_xnode(None, rows, _file=self.file)

        return result
