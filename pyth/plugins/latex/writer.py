"""
Render documents as latex.

For the moment we generate the latex document from the
reStructuredText writer output.
"""

from cStringIO import StringIO
import docutils.core

from pyth import document
from pyth.format import PythWriter
from pyth.plugins.rst.writer import RSTWriter


class LatexWriter(PythWriter):

    @classmethod
    def write(klass, document, target=None):
        """
        convert a pyth document to a latex document
        """
        writer = LatexWriter(document, target)
        return writer.go()

    def __init__(self, doc, target=None):
        self.document = doc
        self.target = target if target is not None else StringIO()

    def go(self):
        rst = RSTWriter.write(self.document).getvalue()
        settings = dict(input_encoding="UTF-8",
                        output_encoding="UTF-8")
        latex = docutils.core.publish_file(StringIO(rst),
                                           writer_name="latex",
                                           settings_overrides=settings)
        self.target.write(latex)
        return self.target
