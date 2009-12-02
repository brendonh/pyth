from pyth.plugins.rtf15.reader import Rtf15Reader
from pyth.plugins.xhtml.writer import XHTMLWriter

doc = Rtf15Reader.read(open('sample.rtf'))

print XHTMLWriter.write(doc, pretty=True).read()


