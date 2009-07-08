"""
Abstract document representation
"""


class Document(object):
    """
    Top-level item. One document is exactly one file.
    Documents consist of a list of paragraphs.
    """
    
    def __init__(self):
        self.paragraphs = []



class Paragraph(object):
    """
    Paragraphs contain zero or more text runs.

    They cannot contain other paragraphs (but see List).

    They have no text markup properties, but may
    have rendering properties (e.g. margins)
    """
    
    def __init__(self):
        self.runs = []



class Text(object):
    """
    Text runs are strings of text with markup properties,
    like 'bold' or 'italic' (or 'hyperlink to ...').

    They are rendered inline (not as blocks).

    They do not inherit their properties from anything.
    """
    
    def __init__(self, text, properties):
        """
        text: A unicode string

        properties: A dictionary of string names to arbitrary values.
                    e.g. {'bold': True}
        """
        self.text = text
        self.properties = properties



class Hyperlink(Text):
    """
    A text run which links to a URL.
    """

    def __init__(self, text, url, properties):
        Text.__init__(self, text, properties)
        self.url = url



class List(Paragraph):
    """
    A list of paragraphs which will be rendered as a bullet list.

    A List is a Paragraph, so Lists can be nested.
    """
    
    def __init__(self):
        self.paragraphs = []
