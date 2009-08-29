"""
Render documents as pdf file using intermediary rst format.
"""

# It rst2pdf fails if we cStringIO !
from StringIO import StringIO
import docutils.core
from rst2pdf import createpdf

from pyth import document
from pyth.format import PythWriter
from pyth.plugins.rst.writer import RSTWriter


class PDFFromRstWriter(PythWriter):

    @classmethod
    def write(klass, document, target=None):
        """
        convert a pyth document to a pdf document using rst
        (reStructuredText) as intermediary format.
        """
        writer = PDFFromRstWriter(document, target)
        return writer.go()

    def __init__(self, doc, target=None):
        self.document = doc
        self.target = target if target is not None else StringIO()

    def go(self):
        rst = RSTWriter.write(self.document).getvalue()
        doctree = docutils.core.publish_doctree(rst)

        print doctree

        sio = StringIO('')
        createpdf.RstToPdf(sphinx=True).createPdf(
                doctree=doctree, output=sio, compressed=False)

        self.target.write(sio.getvalue())
        return self.target
