
from pyth.plugins.python.reader import *
from pyth.plugins.plaintext.writer import PlaintextWriter

doc = PythonReader.read((
    P [
      T(ITALIC, url=u'http://www.google.com') [ u"Hello World, " ],
      u"hee hee hee! ", u"This seems to work"
    ],
    L [
      [unicode(word) for word in ("One", "Two", "Three", "Four")]
    ],
    L [
      u"Introduction",
      LE [
        u"First sentence in the\nsub-section",
        u"Also some other stuff",
        L [
         u"Alpha",
         L [
           u"Beta\nWhomble",
           LE [ u"Beta", u"Whoop\nWhoa" ],
           u"Beta",
         ],
         u"Gamma",
         u"Gamma",
        ],
        u"Final sentence in the sub-section",
      ],
      u"Conclusion",
    ],
    u"That's all, folks!"
))

print PlaintextWriter.write(doc).getvalue()
