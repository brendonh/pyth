"""
Write Pyth documents straight in Python, a la Nevow's Stan.
"""

from pyth.format import PythReader
from pyth.document import *


def _convert(content):
    if isinstance(content, _PythonBase):
        return content.toPyth()
    return content

class PythonReader(PythReader):

    @classmethod
    def read(self, source):
        """
        source: A list of P objects.
        """
        return Document(content=[_convert(c) for c in source])



class _Shortcut(object):
    def __init__(self, key):
        self.key = key

    def asDict(self):
        return dict(((self.key, True),))
        
    
BOLD = _Shortcut("bold")
ITALIC = _Shortcut("italic")
UNDERLINE = _Shortcut("underline")
SUPER = _Shortcut("super")
SUB = _Shortcut("sub")


def _MetaPythonBase():
    """
    Return a metaclass which implements __getitem__,
    allowing e.g. P[...] instead of P()[...]
    """
    
    class MagicGetItem(type):
        def __new__(mcs, name, bases, dict):
            klass = type.__new__(mcs, name, bases, dict)
            mcs.__getitem__ = lambda _, k: klass()[k]
            return klass
            
    return MagicGetItem
        


class _PythonBase(object):
    """
    Base class for Python markup objects, providing
    stan-ish interface
    """

    def __init__(self, *shortcuts, **properties):
        self.properties = properties.copy()
        
        for shortcut in shortcuts:
            self.properties.update(shortcut.asDict())

        self.content = []


    def toPyth(self):
        return self.pythType(self.properties,
                             [_convert(c) for c in self.content])


    def __getitem__(self, item):

        if isinstance(item, (tuple, list)):
            for i in item: self [i]
        elif isinstance(item, int):
            return self.content[item]
        else:
            self.content.append(item)

        return self
    

    def __str__(self):
        return "%s(%s) [ %s ]" % (
            self.__class__.__name__,
            ", ".join("%s=%s" % (k, repr(v)) for (k,v) in self.properties.iteritems()),
            ", ".join(repr(x) for x in self.content))



class P(_PythonBase):
    __metaclass__ = _MetaPythonBase()    
    pythType = Paragraph


class LE(_PythonBase):
    __metaclass__ = _MetaPythonBase()
    pythType = ListEntry

class L(_PythonBase):
    __metaclass__ = _MetaPythonBase()    
    pythType = List


class T(_PythonBase):
    __metaclass__ = _MetaPythonBase()    
    __repr__ = _PythonBase.__str__
    pythType = Text

    def toPyth(self):
        return Text(self.properties, self.content)
