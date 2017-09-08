 README for pyth/tests/rtf-as-html
===================================

This directory contains the reference output for test runs
of the RTF reader pyth.plugins.rtf15.reader files.

The idea for creating these reference files is to
- turn the read results into XHTML,
- wrap that into a proper HTML document file,
- load that file in a web browser, and
- inspect the results visually in comparison to the
  original RTF source.

The content of these files was found correct in this manner
with respect to the current implementation expectation.
Test runs will create corresponding output and compare the
file contents.

For tests that fail (i.e. where the visual inspection finds
relevant differences), the file deposited here is empty.

See the top-level README for current limitations.
Anything documented there is no longer considered a failure.

