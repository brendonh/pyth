from pyth.plugins.xhtml.writer  import XHTMLWriter
from pyth.plugins.rtf15.reader import Rtf15Reader
import sys

if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    filename = "tests/rtfs/sample-with-image.rtf"
source = open(filename, "rb")
doc = Rtf15Reader.read(source)

print XHTMLWriter.write(doc).getvalue()
