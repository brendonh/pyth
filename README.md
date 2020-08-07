pyth3 - Python text markup and conversion
=========================================

Pyth is intended to make it easy to convert marked-up text between different common formats.
This is a (rather incomplete so far) port of pyth 0.6.0 to Python 3.

*Marked-up text* means text which has:

* Paragraphs
* Headings
* Bold, italic, and underlined text
* Hyperlinks
* Bullet lists
* Simple tables
* Very little else


Formats that have (very varying) degrees of support are

* Plain text
* XHTML
* RTF (Rich Text Format)
* PDF (output only)


Design principles/goals
=======================

* Ignore unsupported information in input formats (e.g. page layout)
* Ignore font issues -- output in a single font.
* Ignore specific text sizes, but maintain italics, boldface, subscript/superscript
* Have no dependencies unless they are written in Python, and work
* Make it easy to add support for new formats, by using an architecture based on *plugins* and *adapters*.



Examples
========

See directory `examples`.



Python 3 migration
==================

The code was originally written for Python 2.
It has been partially(!) upgraded to Python 3 compatibility (starting via 'modernize').
This does not mean it will actually work!

pyth.plugins.rtf15.reader has been debugged and now appears to work correctly.
pyth.plugins.xhtml.writer has been debugged and now appears to work correctly.
pyth.plugins.plaintext.writer has been debugged and now appears to work correctly.
Everything else is unknown (or definitely broken on Python 3: even many
of the tests fail)
See directory py3migration for a bit more detail.
(If you find something is broken on Python 2 that worked before, please
either fix it or simply stick to pyth version 0.6.0.)


Limitations
===========

pyth.plugins.rtf15.reader:
- bulleted or enumerated items will be returned
  as plain paragraphs (no indentation, no bullets).
- cannot cope with Symbol font correctly:
  - from MS Word: lower-coderange characters (greek mostly) work
  - from MS Word: higher-coderange characters are missing, because
    Word encodes them in a horribly complicated manner not supported
    by pyth currently
  - from Wordpad: lower- and higher-coderange characters come out in
    the wrong encoding (ANSI, I think)

pyth.plugins.xhtml.writer:
- very limited functionality

pyth.plugins.plaintext.writer:
- very very limited functionality

Others: 
- will not work on Python 3 without some porting love-and-care


Tests
=====

Don't try to run them all, it's frustrating.
`py.test -v test_readrtf15.py` is a good way to run the least frustrating 
subset of them.
It is normal that most others will fail on Python 3.
`test_readrtf15.py` generates test cases dynamically based on
existing input files in `tests/rtfs` and
existing reference output files in `tests/rtf-as-html` and `tests/rtf-as-html`.
The empty or missing output files indicate where functionality is missing,
which nicely indicates possible places to jump in if you want to help.


Dependencies
============

Only the most important two of the dependencies,
are actually declared in `setup.py`, because the others are large, yet
are required only in pyth components not yet ported to Python 3. 
They are:
- `reportlab` for PDFWriter
- `docutils` for LatexWriter 
