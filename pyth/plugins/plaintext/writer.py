"""
Render documents as plaintext.
"""

from pyth import document
from pyth.format import PythWriter

from cStringIO import StringIO

class PlaintextWriter(PythWriter):

    @classmethod
    def write(klass, document, target=None, newline="\n"):
        if target is None:
            target = StringIO()

        writer = PlaintextWriter(document, target, newline)
        return writer.go()


    def __init__(self, doc, target, newline):
        self.document = doc
        self.target = target
        self.newline = newline
        self.indent = -1
        self.paragraphDispatch = {
            document.List: self.list,
            document.Paragraph: self.paragraph
        }


    def go(self):
        for (i, paragraph) in enumerate(self.document.content):
            handler = self.paragraphDispatch[paragraph.__class__]
            handler(paragraph)
            self.target.write("\n")

        # Heh heh, remove final paragraph spacing
        self.target.seek(-2, 1)
        self.target.truncate()

        self.target.seek(0)
        return self.target


    def paragraph(self, paragraph, prefix=""):
        content = []
        for text in paragraph.content:
            content.append(u"".join(text.content))
        content = u"".join(content).encode("utf-8")
            
        for line in content.split("\n"):
            self.target.write("  " * self.indent)
            self.target.write(prefix)
            self.target.write(line)
            self.target.write("\n")
            if prefix: prefix = "  "


    def list(self, list, prefix=None):
        self.indent += 1
        for (i, entry) in enumerate(list.content):           
            for (j, paragraph) in enumerate(entry.content):
                prefix = "* " if j == 0 else "  "
                handler = self.paragraphDispatch[paragraph.__class__]
                handler(paragraph, prefix)
        self.indent -= 1




            
