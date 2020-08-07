from __future__ import absolute_import
from __future__ import print_function
import sys
import os.path

from pyth.plugins.rtf15.reader import Rtf15Reader
from pyth.plugins.xhtml.writer import XHTMLWriter, write_html_file

numargs = len(sys.argv) - 1

if numargs not in [1, 2]:
    print("usage: rtf15 inputfile.rtf [outputdir]")
else:
    inputfile = sys.argv[1]
    doc = Rtf15Reader.read(open(inputfile, "rb"))
    the_output = XHTMLWriter.write(doc, pretty=True).read()
    if numargs == 1:
        print("<!-- ##### RTF file" + inputfile + "as XHTML: -->")
        print(the_output)
    else:
        basename = os.path.basename(inputfile)
        outputdir = sys.argv[2]
        outputfile = os.path.join(outputdir,
                                  os.path.splitext(basename)[0] + ".html")
        write_html_file(outputfile, the_output, print_msg=True)
