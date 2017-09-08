from __future__ import absolute_import
from __future__ import print_function
import glob
import os
import os.path
import unittest

from pyth.plugins.rtf15.reader import Rtf15Reader
from pyth.plugins.xhtml.writer import XHTMLWriter, write_html_file

class TestRtfHTML(unittest.TestCase):
    pass  # will be filled dynamically now:

#--- constants:
#  there is one end2end test case per test input file
mydir = os.path.abspath(os.path.dirname(__file__))
rtfinputsdir = os.path.join(mydir, "rtfs")
referenceoutputdir = os.path.join(mydir, "rtf-as-html")
testoutputdir = os.path.join(mydir, "currentoutput")
inputfilenames = glob.glob(os.path.join(rtfinputsdir, "*.rtf"))

def gen_file_test(basename, testclass):
    """creates one test method and adds it to testclass"""
    def testmethod(self):  # the test method to be added
        inputfilename = os.path.join(rtfinputsdir, basename+".rtf")
        outputfilename = os.path.join(testoutputdir, basename+".html")
        referencefilename = os.path.join(referenceoutputdir, basename+".html")
        #--- obtain reference output or skip test:
        try:
            with open(referencefilename, "rb") as input:
                the_referenceoutput = input.read()
        except OSError:
            print("no", referencefilename, ": skipped")
            return  # TODO: not so great: it will count as a correct test
        #--- read and convert RTF:
        with open(inputfilename, "rb") as input:
            document = Rtf15Reader.read(input)
        the_testoutput = XHTMLWriter.write(document, pretty=True).read()
        #--- compute test output:
        write_html_file(outputfilename, the_testoutput, print_msg=False)
        with open(outputfilename, "rb") as input:
            the_testoutput = input.read()
        #--- check outcome:
        if the_testoutput == the_referenceoutput:
            os.remove(outputfilename)  # assert will succeed, so it is no longer needed
        self.assertEqual(the_testoutput, the_referenceoutput)

    methodname = "test_" + basename.replace('-', '_')  # create Python identifier
    setattr(testclass, methodname, testmethod)  # add test method to test class object

#--- create one test method per RTF input file:
for inputfilename in inputfilenames:
    basename = os.path.splitext(os.path.basename(inputfilename))[0]
    gen_file_test(basename, TestRtfHTML)


if __name__ == '__main__':
    unittest.main(verbosity=1)
