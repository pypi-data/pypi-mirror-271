"""
original script name = untangle.py
Converts xml to python objects.
The only method you need to call is parse()
Partially inspired by xml2obj (http://code.activestate.com/recipes/149368-xml2obj/)
Author: Christian Stefanescu (http://0chris.com)
License: MIT License - http://www.opensource.org/licenses/mit-license.php
"""

from typing import Any
from xml.sax import handler
from xml.sax import make_parser

import os


try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


def _is_string(value: Any) -> bool:
    try:
        from types import StringTypes

        return isinstance(value, StringTypes)
    except ImportError:
        return isinstance(value, str)


def _is_url(string):
    """Checks if the given string starts with 'http(s)'."""
    try:
        return string.startswith("http://") or string.startswith("https://")
    except AttributeError:
        return False


class Element(object):
    """Representation of an XML element."""

    def __init__(self, name, attributes):
        self._name = name
        self._attributes = attributes
        self.children = []
        self.is_root = False
        self.cdata = ""

    def add_child(self, element):
        """Store child elements."""
        self.children.append(element)

    def add_cdata(self, cdata):
        """Store cdata."""
        self.cdata = self.cdata + cdata

    def get_attribute(self, key):
        """Get attributes by key."""
        return self._attributes.get(key)

    def get_elements(self, name=None):
        """Find a child element by name."""
        return [e for e in self.children if e._name == name] if name else self.children

    def __getitem__(self, key):
        return self.get_attribute(key)

    def __getattr__(self, key):
        matching_children = [x for x in self.children if x._name == key]
        if matching_children:
            if len(matching_children) == 1:
                self.__dict__[key] = matching_children[0]
                return matching_children[0]
            else:
                self.__dict__[key] = matching_children
                return matching_children
        else:
            raise AttributeError("'%s' has no attribute '%s'" % (self._name, key))

    def __hasattribute__(self, name):
        if name in self.__dict__:
            return True
        return any(x._name == name for x in self.children)

    def __iter__(self):
        yield self

    def __str__(self) -> str:
        return (
            f"Element {self._name} with attributes {self._attributes}, children {self.children}, and cdata {self.cdata}"
        )

    def __repr__(self) -> str:
        return f"Element(name = {self._name}, attributes = {self._attributes}, cdata = {self.cdata})"

    def __nonzero__(self):
        return self.is_root or self._name is not None

    def __eq__(self, val):
        return self.cdata == val

    def __dir__(self):
        children_names = [x._name for x in self.children]
        return children_names

    def __len__(self):
        return len(self.children)


class Handler(handler.ContentHandler):
    """SAX handler which creates the Python object structure out of ``Element``s."""

    def __init__(self):
        self.root = Element(None, None)
        self.root.is_root = True
        self.elements = []

    def startElement(self, name, attributes):
        name = name.replace("-", "_")
        name = name.replace(".", "_")
        name = name.replace(":", "_")
        attrs = dict()
        for k, v in attributes.items():
            attrs[k] = v
        element = Element(name, attrs)
        if len(self.elements) > 0:
            self.elements[-1].add_child(element)
        else:
            self.root.add_child(element)
        self.elements.append(element)

    def endElement(self, name):
        self.elements.pop()

    def characters(self, cdata):
        self.elements[-1].add_cdata(cdata)


def parse(filename, **parser_features):
    """Interprets the given string as a filename, URL or XML data string, parses it and returns a Python object which
    represents the given document.

    Extra arguments to this function are treated as feature values to pass to ``parser.setFeature()``.
    For example, ``feature_external_ges=False`` will set ``xml.sax.handler.feature_external_ges`` to False, disabling
    the parser's inclusion of external general (text) entities such as DTDs.

    Raises ``ValueError`` if the first argument is None / empty string.
    Raises ``AttributeError`` if a requested xml.sax feature is not found in ``xml.sax.handler``.
    Raises ``xml.sax.SAXParseException`` if something goes wrong  during parsing.
    """

    if filename is None or (_is_string(filename) and filename.strip()) == "":
        raise ValueError("parse() takes a filename, URL or XML string")
    parser = make_parser()
    for feature, value in parser_features.items():
        parser.setFeature(getattr(handler, feature), value)
    sax_handler = Handler()
    parser.setContentHandler(sax_handler)
    if _is_string(filename) and (os.path.exists(filename) or _is_url(filename)):
        parser.parse(filename)
    else:
        parser.parse(filename) if hasattr(filename, "read") else parser.parse(StringIO(filename))
    return sax_handler.root


def _parse_raw(xml):
    """Parses the given string as an XML data string, returning a Python object which represents the document.

    Raises ``ValueError`` if the argument is None / empty string.
    Raises ``xml.sax.SAXParseException`` if something goes wrong during parsing.
    """
    if xml is None or not _is_string(xml) or xml.strip() == "":
        raise ValueError("parse_raw() takes an XML string")
    parser = make_parser()
    sax_handler = Handler()
    parser.setContentHandler(sax_handler)
    parser.parse(StringIO(xml))
    return sax_handler.root
