
"""
unit tests of the pdf writer
"""

import unittest
import subprocess
import tempfile
import os
import sys

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
                print "Make sure that pdftohtml is installed"
                raise
            ret = proc.communicate()[0]
            return ret
        finally:                    # Make sure to remove the tmp file
            file.close()
            os.remove(filename)

    def test_basic(self):
        doc = PythonReader.read([])
        pdf = PDFWriter.write(doc).getvalue()
        html = self.pdf_to_html(pdf)

    def test_paragraph(self):
        doc = PythonReader.read(P[u"the text"])
        pdf = PDFWriter.write(doc).getvalue()
        html = self.pdf_to_html(pdf)
        assert "the text" in html
        
if __name__ == '__main__':
    unittest.main()
