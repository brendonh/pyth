"""
Pyth -- Python text markup and conversion
"""

import os.path

__version__ = '0.5.6'

writerMap = {
    '.rtf': 'pyth.plugins.rtf15.writer.Rtf15Writer',
    '.html': 'pyth.plugins.xhtml.writer.XHTMLWriter',
    '.xhtml': 'pyth.plugins.xhtml.writer.XHTMLWriter',
    '.txt': 'pyth.plugins.plaintext.writer.PlaintextWriter',
    '.pdf': 'pyth.plugins.pdf.writer.PDFWriter',
}


mimeMap = {
    '.rtf': 'application/rtf',
    '.html': 'text/html',
    '.xhtml': 'application/xhtml+xml',
    '.txt': 'text/plain',
}



def write(doc, filename):
    ext = os.path.splitext(filename)[1]
    writer = namedObject(writerMap[ext])
    buff = writer.write(doc)
    buff.seek(0)
    return (buff, mimeMap[ext])


# Stolen from twisted.python.reflect

def namedModule(name):
    """Return a module given its name."""
    topLevel = __import__(name)
    packages = name.split(".")[1:]
    m = topLevel
    for p in packages:
        m = getattr(m, p)
    return m


def namedObject(name):
    """Get a fully named module-global object.
    """
    classSplit = name.split('.')
    module = namedModule('.'.join(classSplit[:-1]))
    return getattr(module, classSplit[-1])
    
