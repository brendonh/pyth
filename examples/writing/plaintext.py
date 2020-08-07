from __future__ import absolute_import
from __future__ import print_function
from pyth.plugins.plaintext.writer import PlaintextWriter
import pythonDoc

doc = pythonDoc.buildDoc()

print(PlaintextWriter.write(doc).getvalue())
