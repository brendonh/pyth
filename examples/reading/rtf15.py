import sys
import os.path

from pyth.plugins.rtf15.reader import Rtf15Reader
from pyth.plugins.xhtml.writer import XHTMLWriter


if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    filename = os.path.normpath(os.path.join(
        os.path.dirname(__file__), 
        '../../tests/rtfs/sample.rtf'))

doc = Rtf15Reader.read(open(filename, "rb"))

print XHTMLWriter.write(doc, pretty=True).read()
