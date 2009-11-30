from pyth.plugins.rtf15.reader import Rtf15Reader
from pyth.plugins.plaintext.writer import PlaintextWriter

doc = Rtf15Reader.read(open('sample.rtf'))

print PlaintextWriter.write(doc).read()


