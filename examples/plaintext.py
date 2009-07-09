from pyth.plugins.plaintext.writer import PlaintextWriter
import pythonDoc

doc = pythonDoc.buildDoc()

print PlaintextWriter.write(doc).getvalue()
