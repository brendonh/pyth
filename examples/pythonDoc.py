# -*- coding: utf-8 -*-

from pyth.plugins.python.reader import *

def buildDoc():
    return PythonReader.read((
      P [
        T(ITALIC) [ u"Hello World, " ],
        u"hee hee hee! ", T(url=u'http://www.google.com') [ u"This seems to work" ]
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
        T(BOLD) [ u"Conclusion" ],
      ],
      u"That's all, folks! 再見!"
    ))
