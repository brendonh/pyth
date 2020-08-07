"""
Render documents as plaintext.
Very scruffy and not very powerful.
Should probably be modified to generate markdown syntax.
"""
from __future__ import absolute_import

from pyth import document
from pyth.format import PythWriter

from six import StringIO

class PlaintextWriter(PythWriter):

    @classmethod
    def write(klass, document, target=None, encoding="utf-8", newline="\n"):
        if target is None:
            target = StringIO()

        writer = PlaintextWriter(document, target, encoding, newline)
        return writer.go()


    def __init__(self, doc, target, encoding, newline):
        self.document = doc
        self.target = target
        self.encoding = encoding
        self.newline = newline
        self.indent = -1
        self.paragraphDispatch = {
            document.List: self.list,
            document.Paragraph: self.paragraph
        }


    def go(self):
        np = len(self.document.content)
        for (i, paragraph) in enumerate(self.document.content):
            handler = self.paragraphDispatch[paragraph.__class__]
            handler(paragraph)
            if i < np - 1:
                self.target.write(self.newline)

        self.target.truncate()

        self.target.seek(0)
        return self.target


    def paragraph(self, paragraph, prefix=""):
        content = []
        for text in paragraph.content:
            content.append("".join(text.content))
        content = "".join(content)

        for line in content.splitlines():
            self.target.write("  " * self.indent)
            self.target.write(prefix)
            self.target.write(line)
            self.target.write(self.newline)
            if prefix: prefix = "  "


    def list(self, list, prefix=None):
        self.indent += 1
        for (i, entry) in enumerate(list.content):
            for (j, paragraph) in enumerate(entry.content):
                prefix = "* " if j == 0 else "  "
                handler = self.paragraphDispatch[paragraph.__class__]
                handler(paragraph, prefix)
        self.indent -= 1





