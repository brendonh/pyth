from pyth import document
from pyth.format import PythWriter

from cStringIO import StringIO

# This map pyth text properties to rml tag names
_tagNames = {'bold': 'b',
             'italic': 'i',
             'underline': 'u',
             'sub': 'sub',
             'super': 'super'}


class PDFWriter(PythWriter):

    @classmethod
    def write(klass, document, target=None):
        """
        convert a pyth document to a pdf document
        """
        # TODO: add a mako template argument
        writer = PDFWriter(document, target)
        return writer.go()

    def __init__(self, doc, target=None):
        self.document = doc
        self.target = target if target is not None else StringIO()

        self.paragraphDispatch = {
            document.List: self._list_to_rml,
            document.Paragraph: self._paragraph_to_rml}

    def go(self):
        elements = [self._element_to_rml(e) for e in self.document.content]
        text = u"".join(elements)
        # TODO add mako processing of the template, and generate the
        # pdf file with trml2pdf
        return self.target

    def _element_to_rml(self, element, style="p", level=0):
        handler = self.paragraphDispatch[type(element)]
        return handler(element, style=style, level=level)

    def _paragraph_to_rml(self, paragraph, style="p", level=0):
        """
        Convert a pyth document paragraph to a valid rml paragraph
        """
        text = u"".join(self._text_to_rml(t) for t in paragraph.content)
        return u'<para style="%s">%s</para>' % (style, text)

    def _text_to_rml(self, text):
        """
        Convert a pyth text object to a valid rml code
        """
        tags = []
        for prop in text.properties:
            if prop in _tagNames:
                tag = _tagNames[prop]
                tags.append(("<%s>" % tag, "</%s>" % tag))

        open_tags = u"".join(tag[0] for tag in tags)
        close_tags = u"".join(tag[1] for tag in reversed(tags))
        content = u"".join(text.content)
        return "%s%s%s" % (open_tags, content, close_tags)

    def _list_to_rml(self, list, style=None, level=0):
        """
        Convert a pyth document list to a valid rml paragraph

        For the moment it will only set the style of the paragraphs to
        "level_N" with N from 1 to the outline level.
        """
        level = level + 1
        text = u"".join(self._list_entry_to_rml(t, level=level)
                        for t in list.content)
        return text

    def _list_entry_to_rml(self, entry, level=0):
        style = "indent_%d" % level
        paragraphs = [self._element_to_rml(e, style=style, level=level)
                      for e in entry.content]
        return u"".join(paragraphs)
