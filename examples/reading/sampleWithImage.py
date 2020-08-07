from __future__ import absolute_import
from __future__ import print_function
from pyth.plugins.rtf15.reader import Rtf15Reader
import sys

if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    filename = "sampleWithImage.rtf"

doc = Rtf15Reader.read(open(filename, "rb"))

print([x.content for x in doc.content])
