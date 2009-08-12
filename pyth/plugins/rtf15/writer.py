"""
Render documents as RTF 1.5

http://www.biblioscape.com/rtf15_spec.htm
"""

from pyth import document
from pyth.format import PythWriter

from cStringIO import StringIO


# XXX Todo -- Make these parameters
PARAGRAPH_SPACING = 150
LIST_ITEM_SPACING = 50

_styleFlags = {
    'bold': r'\b',
    'italic': r'\i',
    'underline': r'\ul',
}


class Rtf15Writer(PythWriter):

    # Calibri is the default font in Office2007.
    # So we'll use that for swiss, and let it fall back
    # to Arial everywhere else.
    fonts = {
        'swiss': 'Calibri',
        'roman': 'Times New Roman',
    }


    @classmethod
    def write(klass, document, target=None, fontFamily='roman'):
        if target is None:
            target = StringIO()

        writer = Rtf15Writer(document, target, fontFamily)
        return writer.go()


    def __init__(self, doc, target, family):
        self.document = doc
        self.target = target

        if family not in self.fonts:
            raise ValueError("Family %s not found (Try %s)" % (
                family, " or ".join("'%s'" % fam for fam in self.fonts)))

        self.fontFamily = family

        self._paragraphDispatch = {
            document.List: self._list,
            document.Paragraph: self._paragraph
        }


    def go(self):
        self.listLevel = -1
        self.addSpacing = None
        
        self.target.write('{')
        self._writeHeader()
        self._writeDocument()
        self.target.write('}')
        return self.target



    # -----------------------------------------------
    # Header section


    def _writeHeader(self):
        # Do this first to get the default font number
        fontTable = self._getFontTable()

        self.target.write(r'\rtf1\ansi\deff%s' % self.fontNumber);

        # Not strictly necessary
        self.target.write('\n')

        for part in (fontTable,
                     self._getColorTable(),
                     self._getStyleSheet(),
                     self._getListTable(),
                     self._getListOverrides(),
                     self._getRevTable()):

            if part:
                self.target.write(part)
                self.target.write('\n')



    def _getFontTable(self):
        output = [r'{\fonttbl']
        for i, (fontFamily, fontName) in enumerate(self.fonts.iteritems()):
            output.append(r'{\f%d\f%s %s;}' % (i, fontFamily, fontName))
            if fontFamily == self.fontFamily:
                self.fontNumber = i

        # We need Symbol for list bullets
        output.append(r'{\f%d\fnil\fprq0\fcharset128 Symbol;}' % (i+1))
        self.symbolFontNumber = i+1
        
        output.append('}')
        return "".join(output)


    def _getColorTable(self):
        # We only need black, and blue (for hyperlinks)
        return (r'{\colortbl;'
                r'\red0\green0\blue0;'
                r'\red0\green0\blue255;}')


    def _getStyleSheet(self):
        # OpenOffice won't render bullets unless there's a stylesheet entry
        # even if it doesn't do anything.
        return r'''{\stylesheet{\s1 List Paragraph;}}'''


    def _getListTable(self):
        # levelnfc23 means bullets (rather than numbering)
        # leveljc0 means left justified
        # levelfollow0 means a tab after the bullet
        output = [r'{\*\listtable{\list\listid1\listtemplateid1']

        for i in range(9):
            output.append((
                r'{\listlevel\levelstartat1\levelnfc23\leveljc0\levelfollow0'
                r'{\leveltext \'01\u61623 ?;}' # The bullet character
                r'\fi-180\f%d' # Indent the bullet left, and use the symbol font
                '}') % self.symbolFontNumber)

        output.append('}}')
        return "".join(output)
    

    def _getListOverrides(self):
        # I have no idea what the point is of this,
        # but we need it.
        return r'{\listoverridetable{\listoverride\listid1\listoverridecount0\ls0}}'


    def _getRevTable(self):
        # Hell no I don't think so
        pass


    # -----------------------------------------------
    # Document section
    

    def _writeDocument(self):

        for part in (self._getInfo(),
                     self._getDocFormat(),
                     self._getSecFormat()):

            if part:
                self.target.write(part)
                self.target.write('\n')


        for paragraph in self.document.content:
            handler = self._paragraphDispatch[paragraph.__class__]
            handler(paragraph)


    def _getInfo(self):
        pass


    def _getDocFormat(self):
        pass


    def _getSecFormat(self):
        pass



    # -----------------------------------------------
    # Content


    def _paragraph(self, paragraph, spacing=PARAGRAPH_SPACING):

        if self.addSpacing is not None:
            self.target.write(r'\sb%d' % self.addSpacing)
            self.addSpacing = None
        
        # Space after the paragraph,
        # expressed in units of god-knows-what
        self.target.write(r'\sa%d{' % spacing)
        
        for text in paragraph.content:
            self._text(text)
            
        self.target.write(r'}\par\pard' '\n')


    def _list(self, lst, spacing=PARAGRAPH_SPACING):
        self.listLevel += 1

        for entry in lst.content:
            for paragraph in entry.content:
                # It doesn't seem like RTF supports multiple paragraphs
                # in the same list item, so just let them be an item each.
                self.target.write(r'\ilvl%d\ls0\li%d\s1' % (
                    self.listLevel, 720*(self.listLevel+1)))
                handler = self._paragraphDispatch[paragraph.__class__]
                handler(paragraph, spacing=LIST_ITEM_SPACING)

        self.listLevel -= 1

        # When going back from a list to regular paragraphs,
        # add some extra spacing to balance the list out.
        if self.listLevel == -1:
            self.addSpacing = 150


    def _text(self, text):

        if 'url' in text.properties:
            self.target.write(
                r'{\field{\*\fldinst HYPERLINK %s}{\fldrslt \*\cf2\ul '
                % text.properties['url'])

        props = []

        if 'super' in text.properties:
            self.target.write('{\up9 ')
        elif 'sub' in text.properties:
            self.target.write('{\dn9 ')

        for prop in text.properties:
            if prop in _styleFlags:
                props.append(_styleFlags[prop])
        
        if props:
            self.target.write("".join(props) + " ")

        
        for run in text.content:                    
            for unichar in run:
                if unichar == '\n':
                    self.target.write(r'\line ')
                    continue

                point = ord(unichar)
                if point < 128:
                    self.target.write(str(unichar))
                else:
                    self.target.write(r'\u%d?' % point)
            
        if props:
            self.target.write("".join("%s0" % p for p in props) + " ")

        if 'super' in text.properties or 'sub' in text.properties:
            self.target.write("}")

        if 'url' in text.properties:
            self.target.write('}}')
