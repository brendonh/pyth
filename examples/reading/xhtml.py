from __future__ import absolute_import
from __future__ import print_function
# -*- coding: utf-8 -*-

from pyth.plugins.xhtml.reader import XHTMLReader
from pyth.plugins.xhtml.writer import XHTMLWriter
import xhtml

from six import StringIO

# A simple xhtml document with limited features.
content = StringIO(r"""
  <div>
    <p><strong>Simple document</strong></p>
    <p><i>this document has

    </i>no hypertext links yet.</p>
    <p><strong>bold text.</strong> <em>italic text.</em></p>
    <p class=important>bold text from css style
      <em> this is bold and italic</em>
    </p>
    <p class=bold> this is bold too</p>
    <p>unicode characters : 你好</p>
    <p style="font-weight: bold">bold too</p>
    <p>
      example<span style="vertical-align: super"> super </span>
      example<span style="vertical-align: sub"> sub </span>
    </p>
    a list
    <ul>
      <li>hello
      test</li>
      <li>bonjour</li>
      <li>guten tag</li>
    </ul>
    <p>
      <a href=http://www.google.com>a link
      </a> single space here.
      <br/>a br tag
    </p>
  </div>
""")

css = """
  .important {font-weight: bold}
  p.bold {font-weight: bold}
  .other {font-weight: normal; color: blue}
"""

if __name__ == '__main__':
    # Parse the document and then reconstruct it using the xhtml
    # writer.
    doc = XHTMLReader.read(content, css)
    print(XHTMLWriter.write(doc).getvalue())
