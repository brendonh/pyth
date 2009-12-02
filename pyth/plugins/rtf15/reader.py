"""
Read documents from RTF 1.5

http://www.biblioscape.com/rtf15_spec.htm

This module is potentially compatible with RTF versions up to 1.9.1,
but may not ignore all necessary control groups.
"""
import string, re, itertools

from pyth import document
from pyth.format import PythReader


_CONTROLCHARS = set(string.ascii_letters + string.digits + "-*")
_DIGITS = set(string.digits)

_CODEPAGES = {
    0: "cp1252",   # ANSI
    1: "cp1252",   # Default (this is wrong, but there is no right)

    # Does Python have built-in support for these? What is it?
    # 2: "42",     # Symbol
    77: "mac-roman", # Mac Roman
    # 78: "10001", # Mac Shift Jis
    # 79: "10003", # Mac Hangul
    # 80: "10008", # Mac GB2312
    # 81: "10002", # Mac Big5
    # 83: "10005", # Mac Hebrew
    84: "mac-arabic", # Mac Arabic
    85: "mac-greek", # Mac Greek
    86: "mac-turkish", # Mac Turkish
    # 87: "10021", # Mac Thai
    # 88: "10029", # Mac East Europe
    # 89: "10007", # Mac Russian

    128: "cp932",  # Shift JIS
    129: "cp949",  # Hangul
    130: "cp1361", # Johab
    134: "cp936",  # GB2312
    136: "cp950",  # Big5
    161: "cp1253", # Greek
    162: "cp1254", # Turkish
    163: "cp1258", # Vietnamese
    177: "cp1255", # Hebrew
    178: "cp1256", # Arabic 
    186: "cp1257", # Baltic
    204: "cp1251", # Russian
    222: "cp874",  # Thai
    238: "cp1250", # Eastern European
    254: "cp437",  # PC 437
    255: "cp850",  # OEM
}


class BackslashEscape(Exception):
    pass


class Rtf15Reader(PythReader):

    @classmethod
    def read(self, source):
        """
        source: A list of P objects.
        """

        reader = Rtf15Reader(source)
        return reader.go()


    def __init__(self, source):
        self.source = source
        self.document = document.Document


    def go(self):
        self.source.seek(0)
        self.group = Group()
        self.charsetTable = None
        self.stack = [self.group]
        self.parse()
        return self.build()


    def parse(self):
        while True:
            next = self.source.read(1)

            if not next:
                break

            if next in '\r\n':
                continue
            if next == '{':
                subGroup = Group(self.group, self.charsetTable)
                self.stack.append(subGroup)
                self.group = subGroup
            elif next == '}':
                subGroup = self.stack.pop()
                subGroup.finalize()

                if subGroup.specialMeaning == 'FONT_TABLE':
                    self.charsetTable = subGroup.charsetTable

                self.group = self.stack[-1]
                self.group.content.append(subGroup)
            elif next == '\\':
                control, digits = self.getControl()
                self.group.handle(control, digits)
            else:
                self.group.char(unicode(next))


    def getControl(self):
        chars = []
        digits = []
        current = chars
        first = True
        while True:
            next = self.source.read(1)

            if not next:
                break

            if first and next == '\\':
                chars.extend("control_symbol")
                digits.append(next)
                break

            if first and next in '\r\n':
                # Special-cased in RTF, equivalent to a \par
                chars.extend("par")
                break

            first = False

            if next == "'":
                # ANSI escape, takes two hex digits
                chars.extend("ansi_escape")
                digits.extend(self.source.read(2))
                break

            if next == ' ':
                # Don't rewind, the space is just a delimiter
                break

            if next not in _CONTROLCHARS:
                # Rewind, it's a meaningful character
                self.source.seek(-1, 1)
                break

            if next in _DIGITS:
                current = digits

            current.append(next)

        return "".join(chars), "".join(digits)


    def build(self):
        doc = document.Document()
       
        #run = []
        #propStack = [{}]
        #block = [None]

        #prevListLevel = None
        #listLevel = None
        #listStack = [doc]

        ctx = BuildContext(doc)

        def flush():
            if ctx.block is None:
                ctx.block = document.Paragraph()

            ctx.block.content.append(
                document.Text(ctx.propStack[-1].copy(), 
                              [u"".join(ctx.run)]))

            ctx.run[:] = []


        def cleanParagraph():
            """
            Compress text runs, remove whitespace at start and end, skip empty blocks, etc
            """

            runs = ctx.block.content

            if not runs:
                ctx.block = None
                return

            joinedRuns = []
            hasContent = False

            for run in runs:

                if run.content[0].strip(): 
                    hasContent = True
                else: 
                    continue

                # Join runs only if their properties match
                if joinedRuns and (run.properties == joinedRuns[-1].properties):
                    joinedRuns[-1].content[0] += run.content[0]
                else:
                    joinedRuns.append(run)

            if hasContent:
                # Strip beginning of paragraph
                joinedRuns[0].content[0] = joinedRuns[0].content[0].lstrip()
                # And then strip the end
                joinedRuns[-1].content[0] = joinedRuns[-1].content[0].rstrip()
                ctx.block.content = joinedRuns
            else:
                ctx.block = None


        for bit in self.group.flatten():

            if isinstance(bit, unicode):
                ctx.run.append(bit)

            elif bit is Push:
                ctx.propStack.append(ctx.propStack[-1].copy())

            elif bit is Pop:
                flush()
                ctx.propStack.pop()

            elif isinstance(bit, Para):

                flush()
                if ctx.block.content:
                    cleanParagraph()
                    if ctx.block is not None:
                        ctx.listStack[-1].append(ctx.block)

                prevListLevel = ctx.listLevel
                ctx.listLevel = bit.listLevel

                if ctx.listLevel > prevListLevel:
                    l = document.List()
                    ctx.listStack.append(l)

                elif ctx.listLevel < prevListLevel:
                    l = ctx.listStack.pop()
                    ctx.listStack[-1].append(l)

                ctx.block = None

            elif bit is Reset:
                flush()
                ctx.propStack[-1].clear()

            elif isinstance(bit, ReadableMarker):
                flush()
                if bit.val:
                    # RTF needs underline markers for hyperlinks,
                    # but nothing else does. If we're in a hyperlink,
                    # ignore underlines.
                    if 'url' in ctx.propStack[-1] and bit.name == 'underline':
                        continue

                    ctx.propStack[-1][bit.name] = bit.val
                else:
                    if bit.name in ctx.propStack[-1]:
                        del propStack[-1][bit.name]

        if ctx.block is not None:
            flush()
            if ctx.block.content:
                cleanParagraph()
                if ctx.block is not None:
                    ctx.listStack[-1].append(ctx.block)

        return doc



class BuildContext(object):
    def __init__(self, doc):
        self.run = []
        self.propStack = [{}]
        self.block = None

        self.listLevel = None
        self.listStack = [doc]




class Group(object):

    def __init__(self, parent=None, charsetTable=None):
        self.parent = parent

        if parent:
            self.props = parent.props.copy()
            self.charset = self.parent.charset
        else:
            self.props = {}
            self.charset = 'cp1252' # ?

        self.specialMeaning = None
        self.skip = False
        self.url = None
        self.currentParaTag = None
        self.destination = False

        self.charsetTable = charsetTable

        self.content = []


    def handle(self, control, digits):

        if control == '*':
            self.destination = True
            return

        handler = getattr(self, 'handle_%s' % control, None)
        if handler is None:
            return

        if digits:
            handler(digits)
        else:
            handler()


    def char(self, char):
        self.content.append(char)


    def _finalize(self):
        
        if self.destination:
            self.skip = True

        if self.specialMeaning is not None:
            self.skip = True

        if self.skip:
            return       

        stuff = []
        i = 0
        while i < len(self.content):
            thing = self.content[i]
            if isinstance(thing, Skip):
                i += thing.count
            else:
                stuff.append(thing)
            i += 1

        self.content = stuff


    # This is only the default,
    # and is overridden by some controls
    finalize = _finalize


    def flatten(self):
        if self.skip:
            return []

        stuff = [Push]
        for thing in self.content:
            if isinstance(thing, Group):
                stuff.extend(thing.flatten())
            else:
                stuff.append(thing)
        stuff.append(Pop)

        return stuff


    def handle_fonttbl(self):
        self.specialMeaning = 'FONT_TABLE'
        self.charsetTable = {}


    def handle_f(self, fontNum):
        if 'FONT_TABLE' in (self.parent.specialMeaning, self.specialMeaning):
            self.fontNum = int(fontNum)
        elif self.charsetTable is not None:
            self.charset = self.charsetTable[int(fontNum)]

            
    def handle_fcharset(self, charsetNum):
        if 'FONT_TABLE' in (self.parent.specialMeaning, self.specialMeaning):
            # Theoretically, \fN should always be before \fcharsetN
            # I don't really expect that will always be true, but let's crash
            # if it's not, and see if it happens in the real world.
            charset = _CODEPAGES.get(int(charsetNum))

            # XXX Todo: Figure out a more graceful way to handle the fact that
            # RTF font declarations can be in their own groups or not
            if self.parent.charsetTable is not None:
                self.parent.charsetTable[self.fontNum] = charset
            else: 
                self.charsetTable[self.fontNum] = charset


    def handle_ansi_escape(self, code):
        try:
            self.content.append(chr(int(code, 16)).decode(self.charset))
        except UnicodeDecodeError:
            self.content.append('?')


    def handle_control_symbol(self, symbol):
        # Ignore ~, -, and _, since they are optional crap.
        if symbol in '\\{}':
            self.content.append(unicode(symbol))


    def handle_u(self, codepoint):
        self.content.append(unichr(int(codepoint)))
        self.content.append(Skip(self.props.get('unicode_skip', 1)))


    def handle_par(self):
        p = Para()
        self.content.append(p)
        self.currentParaTag = p


    def handle_pard(self):
        self.content.append(Reset)


    def handle_plain(self):
        self.content.append(Reset)


    def handle_line(self):
        self.content.append(u"\n")


    def handle_b(self, onOff=None):
        val = onOff in (None, "", "1")
        self.content.append(ReadableMarker("bold", val))


    def handle_i(self, onOff=None):
        val = onOff in (None, "", "1")
        self.content.append(ReadableMarker("italic", val))


    def handle_ul(self, onOff=None):
        val = onOff in (None, "", "1")
        self.content.append(ReadableMarker("underline", val))


    def handle_ilvl(self, level):
        if self.currentParaTag is not None:
            self.currentParaTag.listLevel = level
        else:
            # Well, now we're in trouble. But I'm pretty sure this
            # isn't supposed to happen anyway.
            pass


    def handle_up(self, amount):
        self.content.append(ReadableMarker("super", True))

    def handle_super(self):
        self.content.append(ReadableMarker("super", True))

    def handle_dn(self, amount):
        self.content.append(ReadableMarker("sub", True))

    def handle_sub(self):
        self.content.append(ReadableMarker("sub", True))

    def handle_emdash(self):
        self.content.append(u'\u2014')

    def handle_endash(self):
        self.content.append(u'\u2013')

    def handle_lquote(self):
        self.content.append(u'\u2018')

    def handle_rquote(self):
        self.content.append(u'\u2019')

    def handle_ldblquote(self):
        self.content.append(u'\u201C')

    def handle_rdblquote(self):
        self.content.append(u'\u201D')


    def handle_field(self):
        def finalize():
            if len(self.content) != 2:
                return u""

            destination, content = self.content

            # The destination isn't allowed to contain any controls,
            # so this should be safe.
            # Except when it isn't, like this:
            # {\field{\*\fldinst {\rtlch\fcs1 \af0 \ltrch\fcs0 \insrsid15420660  PAGE   \\* MERGEFORMAT }}
            try:
                destination = u"".join(destination.content)
            except:
                return u""

            match = re.match(ur'HYPERLINK "(.*)"', destination)
            if match:
                content.skip = False
                self.content = [ReadableMarker("url", match.group(1)),
                                content]
            else:
                return u""

        self.finalize = finalize


    def __repr__(self):
        return "G(%s)" % repr(self.content)

    def ignore(self, _=None):
        self.skip = True


    # Header
    handle_filetbl = ignore
    handle_colortbl = ignore
    handle_stylesheet = ignore
    handle_listtable = ignore
    handle_listoverridetable = ignore
    handle_revtbl = ignore

    handle_mmath = ignore

    handle_header = ignore
    handle_footer = ignore
    handle_headerl = ignore
    handle_headerr = ignore
    handle_headerf = ignore
    handle_footerl = ignore
    handle_footerr = ignore
    handle_footerf = ignore


    # Document
    handle_info = ignore
    handle_docfmt = ignore
    handle_pgdsctbl = ignore
    handle_listtext = ignore




class Skip(object):
    def __init__(self, count):
        self.count = count


class ReadableMarker(object):
    def __init__(self, name, val=None):
        self.name = name
        self.val = val

    def __repr__(self):
        if self.val is None:
            return "!%s!" % self.name
        else:
            return "!%s::%s!" % (self.name, self.val)


class Para(ReadableMarker):
    listLevel = None

    def __init__(self):
        ReadableMarker.__init__(self, "Para")

    def __repr__(self):
        return "!Para:%s!" % self.listLevel


Reset = ReadableMarker("Reset")

Push = ReadableMarker("Push")
Pop = ReadableMarker("Pop")
