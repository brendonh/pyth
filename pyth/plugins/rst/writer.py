"""
Render documents as reStructuredText.
"""
from __future__ import absolute_import

from pyth import document
from pyth.format import PythWriter

from cStringIO import StringIO


class RSTWriter(PythWriter):

    @classmethod
    def write(klass, document, target=None):
        if target is None:
            target = StringIO()

        writer = RSTWriter(document, target)
        return writer.go()

    def __init__(self, doc, target):
        self.document = doc
        self.target = target
        self.indent = -1
        self.paragraphDispatch = {document.List: self.list,
                                  document.Paragraph: self.paragraph}

    def go(self):
        for (i, paragraph) in enumerate(self.document.content):
            handler = self.paragraphDispatch[paragraph.__class__]
            handler(paragraph)
            self.target.write("\n")

        # Heh heh, remove final paragraph spacing
        self.target.seek(-2, 1)
        self.target.truncate()

        return self.target

    def text(self, text):
        """
        process a pyth text and return the formatted string
        """
        ret = u"".join(text.content)
        if 'url' in text.properties:
            return u"`%s`_" % ret
        if 'bold' in text.properties:
            return u"**%s**" % ret
        if 'italic' in text.properties:
            return u"*%s*" % ret
        if 'sub' in text.properties:
            return ur"\ :sub:`%s`\ " % ret
        if 'super' in text.properties:
            return ur"\ :sup:`%s`\ " % ret
        return ret

    def paragraph(self, paragraph, prefix=""):
        """
        process a pyth paragraph into the target
        """
        content = []
        for text in paragraph.content:
            content.append(self.text(text))
        content = u"".join(content).encode("utf-8")

        for line in content.split("\n"):
            self.target.write("  " * self.indent)
            self.target.write(prefix)
            self.target.write(line)
            self.target.write("\n")
            if prefix:
                prefix = "  "

        # handle the links
        if any('url' in text.properties for text in paragraph.content):
            self.target.write("\n")
            for text in paragraph.content:
                if 'url' in text.properties:
                    string = u"".join(text.content)
                    url = text.properties['url']
                    self.target.write(".. _%s: %s\n" % (string, url))

    def list(self, list, prefix=None):
        """
        Process a pyth list into the target
        """
        self.indent += 1
        for (i, entry) in enumerate(list.content):
            for (j, paragraph) in enumerate(entry.content):
                prefix = "- " if j == 0 else "  "
                handler = self.paragraphDispatch[paragraph.__class__]
                handler(paragraph, prefix)
                self.target.write("\n")
        self.indent -= 1
