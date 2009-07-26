"""
Read documents from RTF 1.5

http://www.biblioscape.com/rtf15_spec.htm

This module is potentially compatible with RTF versions up to 1.9.1,
but may not ignore all necessary control groups.
"""
import string, re, itertools

from pyth import document
from pyth.format import PythReader


_CONTROLCHARS = set(string.lowercase + string.digits + "-*")
_DIGITS = set(string.digits)


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
        self.stack = [self.group]
        self.parse()
        return self.build()


    def parse(self):
        while True:
            next = self.source.read(1)

            if not next:
                break

            if next == '\n':
                continue
            if next == '{':
                subGroup = Group(self.group)
                self.stack.append(subGroup)
                self.group = subGroup
            elif next == '}':
                subGroup = self.stack.pop()
                subGroup.finalize()
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
        while True:
            next = self.source.read(1)

            if not next:
                break

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

        run = []
        propStack = [{}]
        block = [None]

        prevListLevel = None
        listLevel = None
        listStack = [doc]

        def flush():
            if block[0] is None:
                block[0] = document.Paragraph()

            if run:
                block[0].content.append(document.Text(propStack[-1].copy(), [u"".join(run)]))

            run[:] = []

        for bit in self.group.flatten():

            if isinstance(bit, unicode):
                run.append(bit)

            elif bit is Push:
                propStack.append(propStack[-1].copy())

            elif bit is Pop:
                flush()
                propStack.pop()

            elif isinstance(bit, Para):
                flush()
                listStack[-1].append(block[0])

                prevListLevel = listLevel
                listLevel = bit.listLevel

                if listLevel > prevListLevel:
                    l = document.List()
                    listStack.append(l)

                elif listLevel < prevListLevel:
                    l = listStack.pop()
                    listStack[-1].append(l)

                block[0] = None

            elif bit is Reset:
                flush()
                propStack[-1].clear()

            elif isinstance(bit, ReadableMarker):
                flush()
                if bit.val:

                    # RTF needs underline markers for hyperlinks,
                    # but nothing else does. If we're in a hyperlink,
                    # ignore underlines.
                    if 'url' in propStack[-1] and bit.name == 'underline':
                        continue

                    propStack[-1][bit.name] = bit.val
                else:
                    if bit.name in propStack[-1]:
                        del propStack[-1][bit.name]


        return doc


class Group(object):

    def __init__(self, parent=None):
        if parent:
            self.props = parent.props.copy()
        else:
            self.props = {}

        self.skip = False
        self.url = None
        self.currentParaTag = None

        self.content = []


    def handle(self, control, digits):

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


    def handle_ansi_escape(self, code):
        self.content.append(chr(int(code, 16)).decode("cp1252"))


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

    def handle_super(self, amount):
        self.content.append(ReadableMarker("super", True))

    def handle_dn(self, amount):
        self.content.append(ReadableMarker("sub", True))

    def handle_sub(self, amount):
        self.content.append(ReadableMarker("sub", True))


    def handle_field(self):
        def finalize():
            if len(self.content) != 2:
                return u""

            destination, content = self.content

            # The destination isn't allowed to contain any controls,
            # so this should be safe
            destination = u"".join(destination.content)

            match = re.match(ur'HYPERLINK "(.*)"', destination)
            if match:
                self.content = [ReadableMarker("url", match.group(1)),
                                content]
                self._finalize()
            else:
                return u""

        self.finalize = finalize


    def __repr__(self):
        return "G(%s)" % repr(self.content)

    def ignore(self, _=None):
        self.skip = True


    # Header
    handle_fonttbl = ignore
    handle_filetbl = ignore
    handle_colortbl = ignore
    handle_stylesheet = ignore
    handle_listtable = ignore
    handle_listoverridetable = ignore
    handle_revtbl = ignore

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
