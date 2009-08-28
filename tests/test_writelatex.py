"""
unit tests of the latex writer
"""

import unittest
import subprocess
import tempfile
import os
import sys
import BeautifulSoup

from pyth.plugins.latex.writer import LatexWriter
from pyth.plugins.python.reader import *


class TestWriteLatex(unittest.TestCase):

    def test_basic(self):
        """
        Try to create an empty latex document
        """
        doc = PythonReader.read([])
        latex = LatexWriter.write(doc).getvalue()

    def test_paragraph(self):
        """
        Try a single paragraph document
        """
        doc = PythonReader.read(P[u"the text"])
        latex = LatexWriter.write(doc).getvalue()
        assert "the text" in latex

    def test_bold(self):
        doc = PythonReader.read([P[T(BOLD)[u"bold text"]]])
        latex = LatexWriter.write(doc).getvalue()
        assert r"\textbf{bold text}" in latex, latex

    def test_italic(self):
        doc = PythonReader.read([P[T(ITALIC)[u"italic text"]]])
        latex = LatexWriter.write(doc).getvalue()
        assert r"\emph{italic text}" in latex, latex
