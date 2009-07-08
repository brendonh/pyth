"""
Stuff for format implementations to subclass / use.
"""


class PythReader(object):
    """
    Base class for all Pyth readers.

    Readers must implement these methods.
    """

    @classmethod
    def read(self, source):
        """
        source: An object to read the document from.
        Usually (but not necessarily) a file object.

        Returns: A pyth.document.Document object.
        """
        pass



class PythWriter(object):
    """
    Base class for all Pyth writers.

    Writers must implement these methods.
    """

    @classmethod
    def write(self, document, target=None):
        """
        document: An instance of pyth.document.Document
        
        target: An object to write the document to.
        Usually (but not necessarily) a file object.
        If target is None, return something sensible
        (like a StringIO object)

        Returns: The target object
        """
        pass
