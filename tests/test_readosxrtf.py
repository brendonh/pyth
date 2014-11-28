
# -*- coding: UTF-8 -*-
"""
Unit tests of the rtf15 reader.
"""

import unittest

from pyth.plugins.rtf15.reader import Rtf15Reader
from pyth.plugins.plaintext.writer import PlaintextWriter
from StringIO import StringIO

class TestReadOSXRtf(unittest.TestCase):

    def test_read(self):
        rtf = StringIO("""{\\rtf1\\ansi\\ansicpg1252\\cocoartf1343\\cocoasubrtf160\\cocoascreenfonts1{\\fonttbl\\f0\\fnil\\fcharset222 Thonburi;}
{\\colortbl;\\red255\\green255\\blue255;}
\\pard\\tx560\\tx1120\\tx1680\\tx2240\\tx2800\\tx3360\\tx3920\\tx4480\\tx5040\\tx5600\\tx6160\\tx6720\\pardirnatural\\qc

\\f0\\fs24 \\cf0 \\'b9\\'e9\\'d3\\'b5\\'a1""")
        doc = Rtf15Reader.read(rtf)
        text = PlaintextWriter.write(doc).read()
        print text
        self.assertEquals(u"น้ำตก", text.decode('utf8'))


    def test_read2(self):
        rtf = StringIO("""{\\rtf1\\ansi\\ansicpg1252\\cocoartf1343\\cocoasubrtf160\\cocoascreenfonts1{\\fonttbl\\f0\\fnil\\fcharset222 Thonburi;}
{\\colortbl;\\red255\\green255\\blue255;}
\\pard\\tx560\\tx1120\\tx1680\\tx2240\\tx2800\\tx3360\\tx3920\\tx4480\\tx5040\\tx5600\\tx6160\\tx6720\\pardirnatural\\qc

{\\f0\\fs24 \\cf0 \\'b9\\'e9\\'d3\\'b5\\'a1}""")
        doc = Rtf15Reader.read(rtf)
        text = PlaintextWriter.write(doc).read()
        print text
        self.assertEquals(u"น้ำตก", text.decode('utf8'))