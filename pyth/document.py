"""
Abstract document representation
"""

class _PythBase(object):

    def __init__(self, properties={}, content=[]):
        self.properties = {}
        self.content = []
        
        for (k,v) in properties.iteritems():
            self[k] = v

        for item in content:
            self.append(item)


    def __setitem__(self, key, value):
        if key not in self.validProperties:
            raise ValueError("Invalid %s property: %s" % (self.__class__.__name__, repr(key)))

        self.properties[key] = value


    def append(self, item):
        if not isinstance(item, self.contentType):
            raise TypeError("Wrong content type: %s" % repr(type(item)))

        self.content.append(item)



class Text(_PythBase):
    """
    Text runs are strings of text with markup properties,
    like 'bold' or 'italic' (or 'hyperlink to ...').

    They are rendered inline (not as blocks).

    They do not inherit their properties from anything.
    """

    validProperties = ('bold', 'italic', 'underline', 'url')
    contentType = unicode



class Paragraph(_PythBase):
    """
    Paragraphs contain zero or more text runs.

    They cannot contain other paragraphs (but see List).

    They have no text markup properties, but may
    have rendering properties (e.g. margins)
    """

    validProperties = ()
    contentType = Text



class ListEntry(_PythBase):
    """
    A list of paragraphs representing one item in a list
    """
    validProperties = ()
    contentType = Paragraph


class List(Paragraph):
    """
    A list of paragraphs which will be rendered as a bullet list.

    A List is a Paragraph, so Lists can be nested.
    """

    validProperties = ()
    contentType = ListEntry
    


class Document(_PythBase):
    """
    Top-level item. One document is exactly one file.
    Documents consist of a list of paragraphs.
    """
    
    validProperties = ()
    contentType = Paragraph




