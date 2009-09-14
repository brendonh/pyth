"""
Render documents as pdf file using intermediary latex format.

This is quite experimental.  It relies on xelatext to generate the
pdf (latex doesn't handle utf-8).

We have to make sure xelatex is installed as well as all the
appropriate latex module.
"""

from pyth.format import PythWriter
from pyth.plugins.latex.writer import LatexWriter

import tempfile
import os
import subprocess


class PDFFromLatexWriter(PythWriter):

    @classmethod
    def write(klass, document, target=None):
        """
        convert a pyth document to a pdf document
        """
        writer = PDFFromLatexWriter(document, target)
        return writer.go()

    def __init__(self, doc, target=None):
        """Create a writer that produces a pdf document
        """
        self.document = doc
        self.target = target if target is not None else StringIO()

    def go(self):
        """generate the pdf file from latex intermediary file

        The problem here is that we cannot do that directly from
        python, but we need to run latex from the shell.
        """
        latex = LatexWriter.write(self.document).getvalue()
        # Create a tmp directory for the latex and pdf files
        tmp_dir = tempfile.mkdtemp()
        try:
            # save the latex file
            latex_file = os.path.join(tmp_dir, "out.tex")
            pdf_file = os.path.join(tmp_dir, "out.pdf")
            file = open(latex_file, "w")
            file.write(latex)
            file.close()

            # generate the pdf using xelatex
            command = ["xelatex", "-interaction=nonstopmode",
                       "-output-directory=%s" % tmp_dir, latex_file]
            try:
                proc = subprocess.Popen(command, stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE)
            except OSError:
                print "Make sure that xelatex is installed"
                raise
            proc.communicate()[0]

            # Copy the pdf file into the target
            pdf = open(pdf_file, "rb").read()
            self.target.write(pdf)
        finally:
            # Make sure that whatever happens, we delete the tmp files
            for file in os.listdir(tmp_dir):
                os.remove(os.path.join(tmp_dir, file))
            os.rmdir(tmp_dir)

        return self.target
