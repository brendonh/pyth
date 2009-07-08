
from pyth.plugins.python.reader import *
from pyth.plugins.plaintext.writer import PlaintextWriter

doc = PythonReader.read((
    P [
      T(ITALIC, url=u'http://www.google.com') [ u"Hello World, " ],
      T [ u"hee hee hee! ", u"This seems to work" ]
    ],
    L [ [
      LE [ P [ T [ unicode(word) ] ] ]
      for word in ("One", "Two", "Three", "Four")
    ] ],
    L [
      LE [ P [ T [ u"Introduction" ] ] ],
      LE [
        P [ T [ u"First sentence in the\nsub-section" ] ],
        P [ T [ u"Also some other stuff" ] ],        
        L [
         LE [ P [ T [ u"Alpha" ] ] ],
         LE [ L [
           LE [ P [ T [ u"Beta\nWhomble" ] ] ],
           LE [ P [ T [ u"Beta" ] ], P [ T [ u"Whoop\nWhoa" ] ] ],
           LE [ P [ T [ u"Beta" ] ] ],
         ] ],
         LE [ P [ T [ u"Gamma" ] ] ],
         LE [ P [ T [ u"Gamma" ] ] ],         
        ],
        P [ T [ u"Final sentence in the sub-section" ] ],
      ],
      LE [ P [ T [ u"Conclusion" ] ] ],
    ],
    P [ T [ u"That's all, folks!" ] ]

))

print PlaintextWriter.write(doc).getvalue()
