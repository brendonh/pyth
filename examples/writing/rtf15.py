from __future__ import absolute_import
from __future__ import print_function
from pyth.plugins.rtf15.writer import Rtf15Writer
import pythonDoc

doc = pythonDoc.buildDoc()

print(Rtf15Writer.write(doc).getvalue())
