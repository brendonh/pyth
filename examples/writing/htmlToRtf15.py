from pyth.plugins.xhtml.reader import XHTMLReader
from pyth.plugins.rtf15.writer import Rtf15Writer
import sys

if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    filename = "tests/html/sample-with-image.html"
source = open(filename, "rb")
doc = XHTMLReader.read(source)

print Rtf15Writer.write(doc).getvalue()
