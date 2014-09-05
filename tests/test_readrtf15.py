
"""
Unit tests of the xhtml reader.
"""

import unittest
import pyth.document
from pyth.plugins.rtf15.reader import Rtf15Reader
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO


class TestReadXHTML(unittest.TestCase):

    def test_basic(self):
        """
        Try to read an empty rtf document
        """
        rtf = open('test.rtf', 'rb')
        rtf = rtf.read()
        # Read file content by chunks
        content = StringIO()
        content.write(rtf)

        content.seek(0)
        doc = Rtf15Reader.read(content)
        self.assert_(isinstance(doc.content[0], pyth.document.Paragraph))
        self.assert_(doc.content[2].content[0].content[0],
                     u"[` ~ ! @ # $ % ^ & * ( ) - _ = + [ { ] } \ | ; : ' 0x810x67 , < . > / ?]")


if __name__ == '__main__':
    unittest.main()
