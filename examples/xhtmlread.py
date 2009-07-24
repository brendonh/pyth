# -*- coding: utf-8 -*-

from pyth.plugins.xhtml.reader import XHTMLReader
from pyth.plugins.xhtml.writer import XHTMLWriter
import xhtml

from cStringIO import StringIO

# A simple xhtml document with limited features.
content = StringIO(r"""
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
          "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <title>very simple document</title>

    <style>
        .important {font-weight: bold}
        .other {font-weight: normal; color: blue}
    </style>
  </head>

<body>
  <div>
    <p><strong>Simple document</strong></p>
    <p>this document has no hypertext links yet.</p>
    <p><strong>bold text.</strong> <em>italic text.</em></p>
    <p class=important>bold text from css style
      <em> this is bold and italic</em>
    </p>
    <p>unicode characters : 你好</p>
    a list
    <ul>
      <li>hello</li>
      <li>bonjour</li>
      <li>guten tag</li>
    </ul>
  </div>
</body>
</html>
""")

if __name__ == '__main__':
    # Parse the document and then reconstruct it using the xhtml
    # writer.
    doc = XHTMLReader.read(content)
    print xhtml.docTemplate % XHTMLWriter.write(doc).getvalue()
