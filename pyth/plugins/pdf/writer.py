"""
Render documents as Reportlab PDF stories
"""
from __future__ import absolute_import

from cStringIO import StringIO
import cgi # For escape()

from pyth import document
from pyth.format import PythWriter

from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch

_tagNames = {'bold': 'b',
             'italic': 'i',
             'underline': 'u',
             'sub': 'sub',
             'super': 'super'}

LIST_INDENT = 0.3 * inch
BULLET_INDENT = 0.2 * inch
DEFAULT_PARA_SPACE = 0.2 * inch

BULLET_TEXT = "\xe2\x80\xa2"

class PDFWriter(PythWriter):

    @classmethod
    def write(klass, document, target=None, paragraphStyle=None):
        writer = PDFWriter(document, paragraphStyle)
        story = writer.go()
        
        if target is None:
            target = StringIO()

        doc = SimpleDocTemplate(target)
        doc.build(story)
        return target


    def __init__(self, doc, paragraphStyle=None):
        self.document = doc

        if paragraphStyle is None:
            stylesheet = getSampleStyleSheet()
            paragraphStyle = stylesheet['Normal']
        self.paragraphStyle = paragraphStyle
        self.paragraphStyle.spaceAfter = 0.2 * inch

        self.paragraphDispatch = {
            document.List: self._list,
            document.Paragraph: self._paragraph}


    def go(self):
        self.paragraphs = []
        for para in self.document.content:
            self._dispatch(para)
        return self.paragraphs
            

    def _dispatch(self, para, level=0, **kw):
        handler = self.paragraphDispatch[type(para)]
        return handler(para, level=level, **kw)


    def _paragraph(self, paragraph, level=0, bulletText=None):
        text = u"".join(self._text(t) for t in paragraph.content)
        self.paragraphs.append(Paragraph(text, self.paragraphStyle, bulletText=bulletText))


    def _text(self, text):
        content = cgi.escape(u"".join(text.content))

        tags = []
        for prop, value in list(text.properties.items()):
            if prop == "url":
                tags.append((u'<u><link destination="%s" color="blue">' % value, u"</link></u>"))
            if prop in _tagNames:
                tag = _tagNames[prop]
                tags.append((u"<%s>" % tag, u"</%s>" % tag))

        open_tags = u"".join(tag[0] for tag in tags)
        close_tags = u"".join(tag[1] for tag in reversed(tags))
        return u"%s%s%s" % (open_tags, content, close_tags)


    def _list(self, plist, level=0, bulletText=None):
        for entry in plist.content:
            self._list_entry(entry, level=level+1)


    def _list_entry(self, entry, level):
        first = True
        prevStyle = self.paragraphStyle

        self.paragraphStyle = ParagraphStyle("ListStyle", self.paragraphStyle)

        for para in entry.content:

            if first: 
                bullet = BULLET_TEXT
                self.paragraphStyle.leftIndent = LIST_INDENT * level
                self.paragraphStyle.bulletIndent = (LIST_INDENT * level - 1) + BULLET_INDENT
            else: 
                bullet = None
                self.paragraphStyle.leftIndent = LIST_INDENT * (level + 1)

            self._dispatch(para, level=level, bulletText=bullet)

            first = False

        self.paragraphStyle = prevStyle



