"""
Render documents as XHTML fragments
"""



from pyth import document
from pyth.format import PythWriter
import base64
import re

from cStringIO import StringIO


_tagNames = {
    'bold': 'strong',
    'italic': 'em',
    'underline': 'u', # ?
    'super': 'sup',
    'sub': 'sub',
}


class XHTMLWriter(PythWriter):

    @classmethod
    def write(klass, document, target=None, cssClasses=True, pretty=False):
        if target is None:
            target = StringIO()

        writer = XHTMLWriter(document, target, cssClasses, pretty)
        final = writer.go()
        final.seek(0)

        # Doesn't work all that well -- appends an <?xml ...> tag,
        # and puts line breaks in unusual places for HTML.
        #if pretty:
        #    content = final.read()
        #    final.seek(0)
        #    from xml.dom.ext import PrettyPrint
        #    from xml.dom.ext.reader.Sax import FromXml
        #    PrettyPrint(FromXml(content), final)
        #    final.seek(0)

        return final


    def __init__(self, doc, target, cssClasses=True, pretty=False):
        self.document = doc
        self.target = target
        self.cssClasses = cssClasses
        self.pretty = pretty
        self.paragraphDispatch = {
            document.List: self._list,
            document.Paragraph: self._paragraph
        }
        self.paragraphContentDispatch = {
            document.Text: self._text,
            document.Image: self._image,
        }


    def go(self):

        self.listLevel = -1

        tag = Tag("div")

        for element in self.document.content:
            handler = self.paragraphDispatch[element.__class__]
            tag.content.extend(handler(element))

        tag.render(self.target)
        return self.target


    def _paragraph(self, paragraph):
        p = Tag("p")
        for item in paragraph.content:
            handler = self.paragraphContentDispatch[item.__class__]
            p.content.append(handler(item))

        if self.pretty:
            return [_prettyBreak, p, _prettyBreak]
        else:
            return [p]


    def _list(self, lst):
        self.listLevel += 1

        ul = Tag("ul")

        if self.cssClasses:
            ul.attrs['class'] = 'pyth_list_%s' % self.listLevel

        last_li = None
        for entry in lst.content:
            li = Tag("li")
            for element in entry.content:
                # in practice list elements always have only one content child?
                handler = self.paragraphDispatch[element.__class__]
                if handler == self._list:
                    # this is a sublist, so we shouldn't create an empty li, but rather append ul to prior li.
                    # Lists can't be immediately sublisted (e.g. there must be at least something at outer level)
                    # but if that is not the case the last_li will be None and next line will bomb out, which is a
                    # useful implicit assertion
                    last_li.content.extend(handler(element))
                else:
                    li.content.extend(handler(element))
                    last_li = li
            if li.content:  # li might be empty..
                ul.content.append(li)

        self.listLevel -= 1

        return [ul]


    def _text(self, text):
        if 'url' in text.properties:
            tag = Tag("a")
            tag.attrs['href'] = text.properties['url']
        else:
            tag = Tag(None)

        current = tag

        for prop in ('bold', 'italic', 'underline', 'sub', 'super'):
            if prop in text.properties:
                newTag = Tag(_tagNames[prop])
                current.content.append(newTag)
                current = newTag

        current.content.append(u"".join(text.content))

        return tag

    def _image(self, image):
        if image.properties.get(u'pngblip'):
            tag = Tag("img")
            image_data = bytearray.fromhex(image.content[0])
            base64_image = base64.b64encode(image_data)
            tag.attrs['src'] = "data:image/png;base64,{}".format(base64_image)
            height = image['pichgoal']
            width = image['picwgoal']
            if width or height:
                styles = []
                styles.append(_twips_to_style_px('width', width))
                styles.append(_twips_to_style_px('height', height))
                style = ';'.join(s for s in styles if s)
                if style:
                    tag.attrs['style'] = style
            return tag
        else:
            return Tag(None)


_prettyBreak = object()


class Tag(object):

    def __init__(self, tag, attrs=None, content=None):
        self.tag = tag
        self.attrs = attrs or {}
        self.content = content or []


    def render(self, target):

        if self.tag is not None:
            attrString = self.attrString()
            if attrString:
                attrString = " " + attrString
            target.write('<%s%s>' % (self.tag, attrString))

        for c in self.content:
            if isinstance(c, Tag):
                c.render(target)
            elif c is _prettyBreak:
                target.write('\n')
            else:
                target.write(quoteText(c).encode("utf-8").replace('\n', '<br />'))

        if self.tag is not None:
            target.write('</%s>' % self.tag)


    def attrString(self):
        return " ".join(
            '%s="%s"' % (k, quoteAttr(v))
            for (k, v) in self.attrs.iteritems())


    def __repr__(self):
        return "T(%s)[%s]" % (self.tag, repr(self.content))



def quoteText(text):
    return re.sub(
        u'&(?!(amp|lt|gt);)', u'&amp;', text, flags=re.IGNORECASE).replace(
        u"<", u"&lt;").replace(
        u">", u"&gt;")


def quoteAttr(text):
    return quoteText(text).replace(
        u'"', u"&quot;").replace(
        u"'", u"&apos;")


def _twips_to_style_px(tag, twips):
    try:
        twips = int(twips)
    except ValueError:
        pass
    px = int(round(twips / 15.0))
    return "{}:{}px".format(tag, px)
