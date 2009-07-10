"""
Render documents as XHTML fragments
"""



from pyth import document
from pyth.format import PythWriter

from cStringIO import StringIO


_tagNames = {
    'bold': 'strong',
    'italic': 'em',
    'underline': 'u', # ?
}


class XHTMLWriter(PythWriter):

    @classmethod
    def write(klass, document, target=None, cssClasses=True):
        if target is None:
            target = StringIO()

        writer = XHTMLWriter(document, target, cssClasses)
        return writer.go()


    def __init__(self, doc, target, cssClasses=True):
        self.document = doc
        self.target = target
        self.cssClasses = cssClasses
        self.paragraphDispatch = {
            document.List: self._list,
            document.Paragraph: self._paragraph
        }
        

    def go(self):

        self.listLevel = -1
        
        tag = Tag("div")
        
        for element in self.document.content:
            handler = self.paragraphDispatch[element.__class__]
            tag.content.append(handler(element))

        tag.render(self.target)
        return self.target
    

    def _paragraph(self, paragraph):
        p = Tag("p")
        for text in paragraph.content:
            p.content.append(self._text(text))
        return p


    def _list(self, lst):
        self.listLevel += 1
        
        ul = Tag("ul")

        if self.cssClasses:
            ul.attrs['class'] = 'pyth_list_%s' % self.listLevel
        
        for entry in lst.content:
            li = Tag("li")
            for element in entry.content:
                handler = self.paragraphDispatch[element.__class__]
                li.content.append(handler(element))
            ul.content.append(li)

        self.listLevel -= 1
            
        return ul


    def _text(self, text):
        if 'url' in text.properties:
            tag = Tag("a")
            tag.attrs['href'] = text.properties['url']
        else:
            tag = Tag(None)

        current = tag

        for prop in ('bold', 'italic', 'underline'):
            if prop in text.properties:
                newTag = Tag(_tagNames[prop])
                current.content.append(newTag)
                current = newTag

        current.content.append(u"".join(text.content))

        return tag



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
    return text.replace(
        u"&", u"&amp;").replace(
        u"<", u"&lt;").replace(
        u">", u"&gt;")


def quoteAttr(text):
    return quoteText(text).replace(
        u'"', u"&quot;").replace(
        u"'", u"&apos;")
