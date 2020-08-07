"""
Creates many variants of the same kind of test dynamically, based on
test input files (and usually corresponding reference output files).
Tests with no reference output will then be skipped.
Tests with empty reference output will be marked as expectedFailure.
"""
from __future__ import absolute_import
from __future__ import print_function
import glob
import os
import os.path
import unittest

from pyth.plugins.rtf15.reader import Rtf15Reader
from pyth.plugins.xhtml.writer import XHTMLWriter, write_html_file
from pyth.plugins.plaintext.writer import PlaintextWriter

class TestRtfHTML(unittest.TestCase):
    pass  # will be filled dynamically now:

#--- constants:
#  there is one end2end test case per test input file
mydir = os.path.abspath(os.path.dirname(__file__))
rtfinputsdir = os.path.join(mydir, "rtfs")
testoutputdir = os.path.join(mydir, "currentoutput")
inputfilenames = glob.glob(os.path.join(rtfinputsdir, "*.rtf"))

def gen_file_test(basename, testclass, writer="either 'html' or 'txt'"):
    """creates one test method and adds it to testclass"""
    referenceoutputdir = os.path.join(mydir, "rtf-as-%s" % writer)
    referencefilename = os.path.join(referenceoutputdir, 
                                     "%s.%s" % (basename, writer))
    def testmethod(self):  # the test method to be added
        inputfilename = os.path.join(rtfinputsdir, basename+".rtf")
        outputfilename = os.path.join(testoutputdir, 
                                      "%s.%s" % (basename, writer))
        #--- obtain reference output or skip test:
        with open(referencefilename, "rb") as input:
            the_referenceoutput = input.read()
        #--- read and convert RTF:
        with open(inputfilename, "rb") as input:
            document = Rtf15Reader.read(input)
        if writer == 'html':
            the_testoutput = XHTMLWriter.write(document, pretty=True).read()
            write_html_file(outputfilename, the_testoutput, print_msg=False)
        elif writer == 'txt':
            with open(outputfilename, "wt") as f:
                PlaintextWriter.write(document, f)

        #--- compute test output:
        with open(outputfilename, "rb") as input:
            the_testoutput = input.read()
        #--- check outcome:
        if the_testoutput == the_referenceoutput:
            os.remove(outputfilename)  # assert will succeed, so it is no longer needed
        self.assertEqual(the_testoutput, the_referenceoutput)

    methodname = "test_%s_%s" % (  # create Python identifier
            basename.replace('-', '_'), writer)
    if not os.path.exists(referencefilename):
        # this test cannot be executed because of a missing outcome expectation: 
        testmethod = unittest.skip("no reference output found")(testmethod)
    elif not os.path.getsize(referencefilename):
        # this test is expected to fail, as indicated by empty reference output: 
        testmethod = unittest.expectedFailure(testmethod)
    setattr(testclass, methodname, testmethod)  # add test method to test class object

#--- create one test method per RTF input file:
for inputfilename in inputfilenames:
    basename = os.path.splitext(os.path.basename(inputfilename))[0]
    gen_file_test(basename, TestRtfHTML, "html")
    gen_file_test(basename, TestRtfHTML, "txt")


if __name__ == '__main__':
    unittest.main(verbosity=1)
