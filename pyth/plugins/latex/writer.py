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
    def write(klass, document, target=None, stylesheet=""):
        """
        convert a pyth document to a latex document

        we can specify a stylesheet as a latex document fragment that
        will be inserted after the headers.  This way we can override
        the default style.
        """
        writer = LatexWriter(document, target, stylesheet)
        return writer.go()

    def __init__(self, doc, target=None, stylesheet=""):
        """Create a writer that produce a latex document

        we can specify a stylesheet as a latex document fragment that
        will be inserted after the headers.  This way we can override
        the default style.
        """
        self.document = doc
        self.stylesheet = stylesheet
        self.target = target if target is not None else StringIO()

    @property
    def full_stylesheet(self):
        """
        Return the style sheet that will ultimately be inserted into
        the latex document.

        This is the user given style sheet plus some additional parts
        to add the meta data.
        """
        latex_fragment = r"""
        \usepackage[colorlinks=true,linkcolor=blue,urlcolor=blue]{hyperref}
        \hypersetup{
           pdftitle={%s},
           pdfauthor={%s},
           pdfsubject={%s}
        }
        """ % (self.document.properties.get("title"),
               self.document.properties.get("author"),
               self.document.properties.get("subject"))
        return latex_fragment + self.stylesheet

    def go(self):
        rst = RSTWriter.write(self.document).getvalue()
        settings = dict(input_encoding="UTF-8",
                        output_encoding="UTF-8",
                        stylesheet="stylesheet.tex")
        latex = docutils.core.publish_string(rst,
                                             writer_name="latex",
                                             settings_overrides=settings)
        # We don't want to keep an \input command in the latex file
        latex = latex.replace(r"\input{stylesheet.tex}",
                              self.full_stylesheet)
        self.target.write(latex)
        return self.target
