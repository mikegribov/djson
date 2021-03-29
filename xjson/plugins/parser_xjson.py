# -*- coding: utf-8 -*-
from pyparsing import Char, Literal, StringEnd, Combine, ZeroOrMore, Forward, Group, QuotedString, Suppress, Word, Optional, delimitedList, alphanums, alphas, nums


class ParserXJson:
    def _get_gram(self):
        def get_tok_info(type):
            if (type == 'identifier'):
                return lambda loc, toks: {"type": ('bool' if (toks[0] in ['true', 'false']) else type),
                                          "token": (toks[0] if (len(toks)) else '')}
            else:
                return lambda loc, toks: {"type": type, "token": (toks[0] if (len(toks)) else '')}

        identifier = Word(alphas + '_', alphanums + '_').setParseAction(get_tok_info("identifier"))

        string = (QuotedString("'", escQuote="\'") | QuotedString("\"", escQuote='\\"')).setParseAction(
            get_tok_info("string"))

        key = ((string | identifier)+ Suppress(':')).setParseAction(get_tok_info("key"))

        integer = Combine(Optional(Suppress('+') | '-') + Word(nums)).setParseAction(get_tok_info("integer"))
        floating = Combine(Optional(Suppress('+') | '-') + Word(nums) + '.' + Word(nums) + Optional(Word("eE") + Optional(Suppress('+') | '-') + Word(nums))).setParseAction(get_tok_info("float"))

        func = Forward()
        link = Forward()
        obj = Forward()
        arr = Forward()

        term = (func | link | string | floating| integer  | identifier | obj | arr)
        pair = Group(key + term)

        args = Group(identifier + ZeroOrMore(Suppress(',') + term)).setParseAction(
            get_tok_info("args"))

        func << Group(identifier + Suppress('(') + Optional(args) + Suppress(')')).setParseAction(
            get_tok_info("function"))
        link << Group(
            Suppress('@') + identifier + ZeroOrMore(Suppress('.') + identifier)).setParseAction(
            get_tok_info("link"))
        obj << Group(
            Suppress("{") + Optional(delimitedList(pair)) + Optional(Suppress(",")) + Suppress("}")).setParseAction(
            get_tok_info("object"))
        arr << Group(
            Suppress("[") + Optional(delimitedList(term)) + Optional(Suppress(",")) + Suppress("]")).setParseAction(
            get_tok_info("array"))

        return (obj | arr)

    def __init__(self):
        self.gram = self._get_gram()

    def parse(self, text):
        self.text = text
        self.ast = self.gram.parseString(text)
        return self.ast

    def _pair_to_text(self, node, indent=''):
        result = ''
        if (node[0]["type"] == "key"):
            result += indent + node[0]["token"]["token"] + ": "
            result += self._val_to_text(node[1], indent)
        else:
            pass  # Exception expected  key

        return result

    def _val_to_text(self, node, indent='', from_pair=True):
        result = ''
        tp = node['type']
        token = node['token']

        if (tp == 'string'):
            result += ('' if (from_pair) else indent) + "\"{}\",\n".format(token.replace('"', '\"'))
        elif (tp in ['integer', 'float', 'identifier']):
            result += ('' if (from_pair) else indent) + "{},\n".format(token)

        elif (tp == 'bool'):
            result += ('' if (from_pair) else indent) + "{},\n".format(token.lower())
        elif (tp == 'object'):
            result += "{\n"
            for pair in token:
                result += self._pair_to_text(pair, indent + "\t")
            result += indent + "}\n"
        elif (tp == 'array'):
            result += "[\n"
            for el in token:
                result += self._val_to_text(el, indent + "\t", False)
            result += indent + "]\n"
        else:
            print("non recognized: ", node)

        return result

    def to_text(self):
        return self._pair_to_text(self.ast[0])

    def _pair_to_dict(self, node):
        result = {}
        if (node[0]["type"] == "key"):
            name = node[0]["token"]["token"]
            result[name] = self._val_to_dict(node[1])
        else:
            pass  # Exception expected  key

        return result

    def _link_to_str(self, token):
        result = ''
        for v in token:
            result += v["token"] + '.'

        return result.rstrip('.')

    def _func_to_str(self, token):
        func_name, args = token[0]['token'], token[1]['token']
        return {"type": "function", "name": func_name, "args": args[0]}

    def _val_to_dict(self, node):
        result = None
        if not isinstance(node, dict):
            return
        tp = node['type']
        token = node['token']
        if (tp == 'function'):
            result = self._func_to_str(token)
        elif (tp == 'link'):
            result = {"type": tp, "ref": self._link_to_str(token)}
        elif (tp == 'string'):
            result = str(token)
        elif (tp == 'integer'):
            result = int(token)
        elif (tp == 'float'):
            result = float(token)
        elif (tp == 'identifier'):
            result = {"type": tp, "value": token}
        elif (tp == 'bool'):
            result = (token.lower() == 'true')
        elif (tp == 'object'):
            result = {}
            for pair in token:
                result.update(self._pair_to_dict(pair))
        elif (tp == 'array'):
            result = []
            for el in token:
                result.append(self._val_to_dict(el))
        else:
            print("non recognized: ", node)

        return result

    def to_dict(self):
        return self._val_to_dict(self.ast[0])

