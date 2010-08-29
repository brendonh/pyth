from pyth.plugins.rtf15.reader import Rtf15Reader
from pyth.plugins.xhtml.writer import XHTMLWriter

import sys

if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    filename = "sample.rtf"

doc = Rtf15Reader.read(open(filename, "rb"))

print XHTMLWriter.write(doc, pretty=True).read()
