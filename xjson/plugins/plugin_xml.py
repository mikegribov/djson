from xml.dom import minidom
from xml.parsers.expat import ExpatError

from .base_file import BaseFilePlugin
from ..xnodes import create_xnode, XNode, XDict, XFileError


class PluginXml(BaseFilePlugin):

    def def_extensions(self) -> set:
        return {'xml'}

    def _node_to_dict(self, node: minidom.Node) -> dict:
        """
        <node atr1="val1" atr2="val2></node>
        convert to
        "node": {
            "atr1":"val1",
            "atr2":"val2",
            "atr3":"val3"
        }
        AND
        <node>
            <atr1>val1</atr1>
            <atr2>val1</atr2>
        </node>
        ***  will be convert to
        "node": {
            "atr1":"val1",
            "atr2":"val2",
            "atr3":"val3"
        }
        //////////////////////////////////////////////////
        <node>
            <row>element1</row>
            <row>element2</row>
            <row>element3</row>
        </node>
        ***  will be convert to
        "node":["element1","element2", "element3"]
        //////////////////////////////////////////////////
        <node>
            <subnode>subnode value</subnode>
            <row>element1</row>
            <row>element2</row>
            <row>element3</row>
        </node>
        ***  will be convert to
        "node":{
            "subnode": "subnode value",
            "row": ["element1","element2", "element3"]
        }

        """
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
        values = {}
        for _node in node.childNodes:
            if isinstance(_node, minidom.Element):
                name = _node.tagName
                text = _node.firstChild
                if text is not None:
                    text = text.data.strip()
                    if text == '':
                        text = None
                if text is None:
                    value = self._node_to_dict(_node)
                else:
                    if no_attributes:
                        result['#text'] = text
                        continue
                    else:
                        value = text
                if name in values:
                    values[name].append(value)
                else:
                    values[name] = [value]

        if len(values) == 1:
            result = values[list(values.keys())[0]]
        else:
            for name in values:
                value = values[name]
                if len(value) == 1:
                    value = value[0]
                result[name] = value
        #result[name] = self._node_to_dict(_node)

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
