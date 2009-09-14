from pyth.plugins.rtf15.reader import Rtf15Reader
from pyth.plugins.xhtml.writer import XHTMLWriter

doc = Rtf15Reader.read(open('lasker.rtf'))

print XHTMLWriter.write(doc, pretty=True).getvalue()


