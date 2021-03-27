from xml.dom import minidom
from xml.parsers.expat import ExpatError

from .base_file import BaseFilePlugin
from ..xnodes import create_xnode, XNode, XDict, XFileError


class PluginXml(BaseFilePlugin):

    def def_extensions(self) -> set:
        return {'xml'}


    def _node_to_dict(self, node: minidom.Node) -> dict:
        result = {}
        if isinstance(node, minidom.Document):
            if node.hasChildNodes():
                return self._node_to_dict(node.childNodes[0])
            else:
                return XDict()
        if not isinstance(node, minidom.Element):
            return XDict()
        attributes = node.attributes
        if attributes is None:
            no_attributes = True
        else:
            no_attributes = False
            result = dict(attributes.items())
        for _node in node.childNodes:
            if isinstance(_node, minidom.Element):
                name = _node.tagName
                text = _node.firstChild
                if text is not None:
                    text = text.data.strip()
                    if text == '':
                        text = None
                if text is None:
                    result[name] = self._node_to_dict(_node)
                else:
                    if no_attributes:
                        result['#text'] = text
                    else:
                        result[name] = text
        return result

    def xml_to_dict(self, content: str) -> dict:
        xml = minidom.parseString(content)
        return self._node_to_dict(xml)

    def load(self, content) -> XNode:
        if content.strip() == '':
            result = XDict(_file=self.file)
        else:
            try:
                result = create_xnode(None, self.xml_to_dict(content), _file=self.file)

            except ExpatError as ex:
                result = XFileError(name=ex, _file=self.file)
        return result
