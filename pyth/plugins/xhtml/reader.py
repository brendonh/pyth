"""
Read documents from xhtml
"""

import BeautifulSoup

from pyth import document
from pyth.format import PythReader
from pyth.plugins.xhtml.css import CSS


class XHTMLReader(PythReader):

    @classmethod
    def read(self, source):
        reader = XHTMLReader(source)
        return reader.go()

    def __init__(self, source):
        self.source = source
        self.css = CSS()

    def go(self):
        soup = BeautifulSoup.BeautifulSoup(self.source)
        doc = document.Document()
        if soup.style:
            self.css = CSS(soup.style.string.strip())
        self.process_into(soup.body, doc)
        return doc

    def is_bold(self, node):
        """
        Return true if the BeautifulSoup node needs to be rendered as
        bold.
        """
        return (node.findParent(['b', 'strong']) is not None or
                self.css.is_bold(node.parent))

    def is_italic(self, node):
        """
        Return true if the BeautifulSoup node needs to be rendered as
        italic.
        """
        return node.findParent('em') is not None

    def process_text(self, node):
        """
        Return a pyth Text object from a BeautifulSoup node or None if
        the text is empty.
        """
        assert isinstance(node, BeautifulSoup.NavigableString)
        text = node.string.strip()
        if not text:
            return
        properties=dict()
        if self.is_bold(node):
            properties['bold'] = True
        if self.is_italic(node):
            properties['italic'] = True
        content=[node.string]
        return document.Text(properties, content)

    def process_into(self, node, obj):
        """
        Process a BeautifulSoup node and fill its elements into a pyth
        base object.
        """
        if isinstance(node, BeautifulSoup.NavigableString):
            text = self.process_text(node)
            if text:
                obj.append(text)
            return
        if node.name == 'p':
            # add a new paragraph into the pyth object
            new_obj = document.Paragraph()
            obj.append(new_obj)
            obj = new_obj
        elif node.name == 'ul':
            # add a new list
            new_obj = document.List()
            obj.append(new_obj)
            obj = new_obj
        elif node.name == 'li':
            # add a new list entry
            new_obj = document.ListEntry()
            obj.append(new_obj)
            obj = new_obj
        for child in node:
            self.process_into(child, obj)
