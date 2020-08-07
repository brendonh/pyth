"""
unit tests of the pdf writer
"""
from __future__ import absolute_import
from __future__ import print_function

import unittest
import subprocess
import tempfile
import os

from bs4 import BeautifulSoup

from pyth.plugins.pdf.writer import PDFWriter
from pyth.plugins.python.reader import *


class TestWritePDF(unittest.TestCase):

    def pdf_to_html(self, pdf):
        """
        We are using pdftohtml to convert the pdf document to an html
        document.

        Since it is difficult to check a pdf document, this allow us
        to first convert it into html, and then perform the checks on
        this html document.
        """
        # pdftohtml needs its input from a file so we first save the
        # pdf into a temporary file.
        _, filename = tempfile.mkstemp(suffix='.pdf')
        file = open(filename, "wb")
        try:
            file.write(pdf)
            file.close()
            command = ["pdftohtml", "-stdout", filename]
            try:
                proc = subprocess.Popen(command, stdout=subprocess.PIPE)
            except OSError:
                print("Make sure that pdftohtml is installed")
                raise
            ret = proc.communicate()[0]
            return ret
        finally:                    # Make sure to remove the tmp file
            file.close()
            os.remove(filename)

    def test_basic(self):
        """
        Try to create an empty pdf document
        """
        doc = PythonReader.read([])
        pdf = PDFWriter.write(doc).getvalue()
        html = self.pdf_to_html(pdf)

    def test_paragraph(self):
        """
        Try a simple document with one paragraph
        """
        doc = PythonReader.read(P[u"the text"])
        pdf = PDFWriter.write(doc).getvalue()
        html = self.pdf_to_html(pdf)
        assert "the text" in html

    def test_bold(self):
        doc = PythonReader.read([P[T(BOLD)[u"bold text"]]])
        pdf = PDFWriter.write(doc).getvalue()
        html = self.pdf_to_html(pdf)
        soup = BeautifulSoup(html)
        node = soup.find("b")
        assert node
        assert node.string == "bold text"

    def test_italic(self):
        doc = PythonReader.read([P[T(ITALIC)[u"italic text"]]])
        pdf = PDFWriter.write(doc).getvalue()
        html = self.pdf_to_html(pdf)
        soup = BeautifulSoup(html)
        node = soup.find("i")
        assert node
        assert node.string == "italic text"

    def test_latex(self):
        doc = PythonReader.read(P[u"the-text"])
        pdf = PDFWriter.write(doc).getvalue()
        html = self.pdf_to_html(pdf)
        assert "the-text" in html, html

    def test_rst(self):
        doc = PythonReader.read(P[u"the-text"])
        pdf = PDFWriter.write(doc).getvalue()
        print(pdf)
        html = self.pdf_to_html(pdf)
        assert "the-text" in html, html


if __name__ == '__main__':
    unittest.main()
