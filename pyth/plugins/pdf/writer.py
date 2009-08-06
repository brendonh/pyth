"""
Render documents as pdf file.

For the moment this writer will first create an intermediary reportlab
rml document, and then use trml2pdf to generate the actual pdf file.

We can customize the rml document by providing a mako template to the
writer.  The mako template is processed with a 'document' argument
that is a pyth.plugins.pdf.writer.Document object.
"""

from pyth import document
from pyth.format import PythWriter
from pyth.plugins.pdf.template import default_template as _default_template

from cStringIO import StringIO
import mako.template
import trml2pdf

# This map pyth text properties to rml tag names
_tagNames = {'bold': 'b',
             'italic': 'i',
             'underline': 'u',
             'sub': 'sub',
             'super': 'super'}


class Paragraph(object):
    """
    Paragraphs can be used in the mako template

    They contains :
    - text : the text of the paragraph (with rml markup tags)
    - level : the indentation level of the paragraph
    """
    def __init__(self, text, level=0):
        self.text = text
        self.level = level

    def __repr__(self):
        return repr(self.text)


class Document(object):
    """
    The structure that will be passed to the mako template
    """

    def __init__(self, paragraphs):
        self.paragraphs = paragraphs

    def __repr__(self):
        return repr(self.paragraphs)


class PDFWriter(PythWriter):

    @classmethod
    def write(klass, document, target=None):
        """
        convert a pyth document to a pdf document
        """
        # TODO: add a mako template argument
        writer = PDFWriter(document, target)
        return writer.go()

    def __init__(self, doc, template=None, target=None):
        self.document = doc
        template = template or _default_template
        self.template = mako.template.Template(
            template,
            output_encoding='utf-8',
            default_filters=['decode.utf8'])

        self.target = target if target is not None else StringIO()

        self.paragraphDispatch = {
            document.List: self._list,
            document.Paragraph: self._paragraph}

    def go(self):
        # generate the list of Paragraph instances
        paragraphs = []
        for e in self.document.content:
            paragraphs += self._element(e)
        document = Document(paragraphs)

        # generate the rml file from the mako template
        rml = self.template.render(document=document)

        # Generate the pdf document
        trml2pdf.trml2pdf.encoding = "UTF-8"
        pdf = trml2pdf.parseString(rml)
        self.target.write(pdf)

        return self.target

    def _element(self, element, level=0):
        """
        convert a pyth element (list or paragraph) to a list of
        Paragraph instances
        """
        handler = self.paragraphDispatch[type(element)]
        return handler(element, level=level)

    def _paragraph(self, paragraph, level=0):
        """
        Convert a pyth document paragraph to a list of Paragraph
        instances
        """
        text = u"".join(self._text(t) for t in paragraph.content)
        return [Paragraph(text, level)]

    def _text(self, text):
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

    def _list(self, list, level=0):
        """
        Convert a pyth document list to a list of Paragraph objects
        """
        level = level + 1
        paragraphs = []
        for t in list.content:
            paragraphs += self._list_entry(t, level=level)
        return paragraphs

    def _list_entry(self, entry, level=0):
        """
        Convert a python document list entry to a list of Paragraph
        objects
        """
        paragraphs = []
        for e in entry.content:
            paragraphs += self._element(e, level=level)
        return paragraphs
