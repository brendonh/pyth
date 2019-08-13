
"""
Unit tests of the xhtml reader.
"""

import unittest

import pyth.document
from pyth.plugins.xhtml.reader import XHTMLReader


class TestReadXHTML(unittest.TestCase):

    def test_basic(self):
        """
        Try to read an empty xhtml document
        """
        xhtml = "<div></div>"
        doc = XHTMLReader.read(xhtml)
        self.assert_(isinstance(doc, pyth.document.Document))
        self.assert_(not doc.content)

    def test_paragraphs(self):
        """
        Try to read a simple xhtml document containing tree paragraphs
        """
        xhtml = "<div><p>p0</p><p>p1</p><p>p2</p></div>"
        doc = XHTMLReader.read(xhtml)
        self.assert_(len(doc.content) == 3)
        for i, p in enumerate(doc.content):
            self.assert_(isinstance(p, pyth.document.Paragraph))
            self.assert_(len(p.content) == 1)
            self.assert_(isinstance(p.content[0], pyth.document.Text))
            text = p.content[0]
            self.assert_(len(text.content) == 1)
            self.assert_(text.content[0] == 'p%d' % i)

    def test_bold(self):
        """
        Try to read a paragraph containing bold text
        """
        xhtml = "<div><p><b>bold</b></p></div>"
        doc = XHTMLReader.read(xhtml)
        text = doc.content[0].content[0]
        assert text['bold']

    def test_italic(self):
        """
        Try to read a paragraph containing italic text
        """
        xhtml = "<div><p><i>italic</i></p></div>"
        doc = XHTMLReader.read(xhtml)
        text = doc.content[0].content[0]
        assert text['italic']

    def test_underline(self):
        """
        Try to read a paragraph containing underline
        """
        xhtml = "<div><p><u>sub</u></p></div>"
        doc = XHTMLReader.read(xhtml)
        text = doc.content[0].content[0]
        assert text['underline']

    def test_underline_styling(self):
        """
        Try to read a paragraph containing underline via CSS
        """
        xhtml = '<div><p style="text-decoration: underline;">underline</p></div>'
        doc = XHTMLReader.read(xhtml)
        text = doc.content[0].content[0]
        assert text['underline']

    def test_sub(self):
        """
        Try to read a paragraph containing subscript
        """
        xhtml = "<div><p><sub>sub</sub></p></div>"
        doc = XHTMLReader.read(xhtml)
        text = doc.content[0].content[0]
        assert text['sub']

    def test_sup(self):
        """
        Try to read a paragraph containing supscript
        """
        xhtml = "<div><p><sup>super</sup></p></div>"
        doc = XHTMLReader.read(xhtml)
        text = doc.content[0].content[0]
        assert text['super']

    def test_url(self):
        """
        Try to read a paragraph containing an url
        """
        xhtml = '<div><p><a href="http://google.com">link</a></p></div>'
        doc = XHTMLReader.read(xhtml)
        text = doc.content[0].content[0]
        assert text['url'] == "http://google.com"

    def test_inline_png(self):
        pixels = 50
        twips = pixels * 15
        height = width = str(twips)  # in retrospect choosing a square image wasn't a great idea :)
        with open('tests/html/sample-with-image.html', 'rb') as xhtml:
            doc = XHTMLReader.read(xhtml)
            image = next(node.content[0] for node in doc.content if isinstance(node.content[0], pyth.document.Image))
            self.assertEquals(image.content[0][1:4], u'PNG')
            self.assertEquals(image['pngblip'], True)
            self.assertEquals(image['pich'], height)
            self.assertEquals(image['pichgoal'], height)
            self.assertEquals(image['picw'], width)
            self.assertEquals(image['picwgoal'], width)
            self.assertEquals(image['picscaley'], '100')
            self.assertEquals(image['picscalex'], '100')


if __name__ == '__main__':
    unittest.main()
