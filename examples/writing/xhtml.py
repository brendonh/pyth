from __future__ import absolute_import
from __future__ import print_function
from pyth.plugins.xhtml.writer import XHTMLWriter
import pythonDoc


docTemplate = '''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <title>Pyth document</title>
  <style type="text/css">body { font-family: Verdana; }</style>
</head>
<body>
%s
</body>
</html>
'''


if __name__ == "__main__":
    doc = pythonDoc.buildDoc()
    print(docTemplate % XHTMLWriter.write(doc, pretty=True).getvalue())
