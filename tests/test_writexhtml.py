import os
import unittest
from pyth.plugins.rtf15.reader import Rtf15Reader
from pyth.plugins.xhtml.writer import XHTMLWriter
from pyth.document import Document, Paragraph, Text

class TestHtmlWithImage(unittest.TestCase):

    def test_inline_png(self):
        sample_with_image = os.path.join(os.path.abspath(os.path.dirname(__file__)), "rtfs", "sample-with-image.rtf")
        with open(sample_with_image, 'rb') as rtf:
            source = Rtf15Reader.read(rtf)
            doc = XHTMLWriter.write(source).getvalue()
            self.assertIn('<img src="data:image/png;base64,', doc)
            self.assertIn('width:50px', doc)
            self.assertIn('height:50px', doc)


    def test_underline(self):
        text = Text(content=[u'Underlined'], properties={'underline': True})
        para = Paragraph(content=[text])
        doc = Document(content=[para])
        result = XHTMLWriter.write(doc).getvalue()
        self.assertIn('<u>Underlined</u>', result)


if __name__ == '__main__':
    unittest.main()
