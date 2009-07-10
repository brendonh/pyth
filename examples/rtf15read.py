from pyth.plugins.rtf15.reader import Rtf15Reader
from pyth.plugins.xhtml.writer import XHTMLWriter

from cStringIO import StringIO

content = StringIO(r"""{\rtf1\ansi\deff1\adeflang1025
{\fonttbl{\f0\froman\fprq2\fcharset0 Times New Roman;}{\f1\froman\fprq2\fcharset0 Calibri;}{\f2\fswiss\fprq2\fcharset0 Arial;}{\f3\fnil\fprq0\fcharset128 Symbol;}{\f4\fmodern\fprq1\fcharset128 Courier New;}{\f5\fnil\fprq0\fcharset128 Wingdings;}{\f6\fnil\fprq2\fcharset0 DejaVu Sans;}{\f7\fnil\fprq2\fcharset0 ;}{\f8\fnil\fprq2\fcharset0 Courier New;}}
{\colortbl;\red0\green0\blue0;\red0\green0\blue255;\red128\green128\blue128;}
{\stylesheet{\s1\sa200\sl276\slmult1{\*\hyphen2\hyphlead2\hyphtrail2\hyphmax0}\ql\rtlch\af7\afs22\lang1025\ltrch\dbch\af6\langfe1033\hich\f1\fs22\lang1033\loch\f1\fs22\lang1033\snext1 Normal;}
{\s2\sb240\sa120\keepn\sl276\slmult1{\*\hyphen2\hyphlead2\hyphtrail2\hyphmax0}\ql\rtlch\af6\afs28\lang1025\ltrch\dbch\langfe1033\hich\f2\fs28\lang1033\loch\f2\fs28\lang1033\sbasedon1\snext3 Heading;}
{\s3\sa120\sl276\slmult1{\*\hyphen2\hyphlead2\hyphtrail2\hyphmax0}\ql\rtlch\af7\afs22\lang1025\ltrch\dbch\af6\langfe1033\hich\f1\fs22\lang1033\loch\f1\fs22\lang1033\sbasedon1\snext3 Body Text;}
{\s4\sa120\sl276\slmult1{\*\hyphen2\hyphlead2\hyphtrail2\hyphmax0}\ql\rtlch\af7\afs22\lang1025\ltrch\dbch\af6\langfe1033\hich\f1\fs22\lang1033\loch\f1\fs22\lang1033\sbasedon3\snext4 List;}
{\s5\sb120\sa120\sl276\slmult1{\*\hyphen2\hyphlead2\hyphtrail2\hyphmax0}\ql\rtlch\af7\afs24\lang1025\ai\ltrch\dbch\af6\langfe1033\hich\f1\fs24\lang1033\i\loch\f1\fs24\lang1033\i\sbasedon1\snext5 caption;}
{\s6\sa200\sl276\slmult1{\*\hyphen2\hyphlead2\hyphtrail2\hyphmax0}\ql\rtlch\af7\afs22\lang1025\ltrch\dbch\af6\langfe1033\hich\f1\fs22\lang1033\loch\f1\fs22\lang1033\sbasedon1\snext6 Index;}
{\s7\li720\ri0\lin720\rin0\fi0\sa200\sl276\slmult1{\*\hyphen2\hyphlead2\hyphtrail2\hyphmax0}\ql\rtlch\af7\afs22\lang1025\ltrch\dbch\af6\langfe1033\hich\f1\fs22\lang1033\loch\f1\fs22\lang1033\sbasedon1\snext7 List Paragraph;}
{\*\cs9\cf0\rtlch\af7\afs22\lang1025\ltrch\dbch\af6\langfe1033\hich\f1\fs22\lang1033\loch\f1\fs22\lang1033 Default Paragraph Font;}
{\*\cs10\cf0\rtlch\af7\afs22\lang1025\ltrch\dbch\af6\langfe1033\hich\f1\fs22\lang1033\loch\f1\fs22\lang1033 DocumentMap;}
{\*\cs11\cf0\rtlch\af7\afs22\lang1025\ltrch\dbch\af6\langfe1033\hich\f1\fs22\lang1033\loch\f1\fs22\lang1033 No List;}
{\*\cs12\cf0\rtlch\af7\afs22\lang1025\ltrch\dbch\af6\langfe1033\hich\f1\fs22\lang1033\loch\f1\fs22\lang1033\sbasedon9 storyhead;}
{\*\cs13\cf2\ul\ulc0\rtlch\af7\afs22\lang1025\ltrch\dbch\af6\langfe1033\hich\f1\fs22\lang1033\loch\f1\fs22\lang1033\sbasedon9 Internet link;}
{\*\cs14\cf0\rtlch\af8\afs22\lang1025\ltrch\dbch\af6\langfe1033\hich\f1\fs22\lang1033\loch\f1\fs22\lang1033 ListLabel 1;}
}{\*\listtable{\list\listtemplateid1
{\listlevel\levelnfc23\leveljc0\levelstartat1\levelfollow0{\leveltext \'01\u61623 ?;}{\levelnumbers;}\f3\fi-360\li720}
{\listlevel\levelnfc23\leveljc0\levelstartat1\levelfollow0{\leveltext \'01\u111 ?;}{\levelnumbers;}\f8\f4\fi-360\li1440}
{\listlevel\levelnfc23\leveljc0\levelstartat1\levelfollow0{\leveltext \'01\u61607 ?;}{\levelnumbers;}\f5\fi-360\li2160}
{\listlevel\levelnfc23\leveljc0\levelstartat1\levelfollow0{\leveltext \'01\u61623 ?;}{\levelnumbers;}\f3\fi-360\li2880}
{\listlevel\levelnfc23\leveljc0\levelstartat1\levelfollow0{\leveltext \'01\u111 ?;}{\levelnumbers;}\f8\f4\fi-360\li3600}
{\listlevel\levelnfc23\leveljc0\levelstartat1\levelfollow0{\leveltext \'01\u61607 ?;}{\levelnumbers;}\f5\fi-360\li4320}
{\listlevel\levelnfc23\leveljc0\levelstartat1\levelfollow0{\leveltext \'01\u61623 ?;}{\levelnumbers;}\f3\fi-360\li5040}
{\listlevel\levelnfc23\leveljc0\levelstartat1\levelfollow0{\leveltext \'01\u111 ?;}{\levelnumbers;}\f8\f4\fi-360\li5760}
{\listlevel\levelnfc23\leveljc0\levelstartat1\levelfollow0{\leveltext \'01\u61607 ?;}{\levelnumbers;}\f5\fi-360\li6480}\listid1}
}{\listoverridetable{\listoverride\listid1\listoverridecount0\ls0}}

{\info{\creatim\yr0\mo0\dy0\hr0\min0}{\revtim\yr0\mo0\dy0\hr0\min0}{\printim\yr0\mo0\dy0\hr0\min0}{\comment StarWriter}{\vern6800}}\deftab709
{\*\pgdsctbl
{\pgdsc0\pgdscuse195\pgwsxn12240\pghsxn15840\marglsxn1440\margrsxn1440\margtsxn1440\margbsxn1440\pgdscnxt0 Standard;}}
\paperh15840\paperw12240\margl1440\margr1440\margt1440\margb1440\sectd\sbknone\pgwsxn12240\pghsxn15840\marglsxn1440\margrsxn1440\margtsxn1440\margbsxn1440\ftnbj\ftnstart1\ftnrstcont\ftnnar\aenddoc\aftnrstcont\aftnstart1\aftnnrlc
\pard\plain \ltrpar\s1\sl276\slmult1{\*\hyphen2\hyphlead2\hyphtrail2\hyphmax0}\sa200\ql\rtlch\af7\afs22\lang1025\ltrch\dbch\af6\langfe1033\hich\f1\fs22\lang1033\loch\f1\fs22\lang1033{\rtlch \ltrch\loch\f1\fs22\lang1033\i0\b0\ltrch\dbch\hich\b\loch\b Louis J. Pt\'e1\u269\'3fek, M.D.}
\par \pard\plain \ltrpar\s1\sl276\slmult1{\*\hyphen2\hyphlead2\hyphtrail2\hyphmax0}\sa200\ql\rtlch\af7\afs22\lang1025\ltrch\dbch\af6\langfe1033\hich\f1\fs22\lang1033\loch\f1\fs22\lang1033{\rtlch \ltrch\loch\f1\fs22\lang1033\i0\b0{\ltrch\dbch\hich\b\loch\b Italics, accented letters, em dashes:}}{\rtlch \ltrch\loch\f1\fs22\lang1033\i0\b0  Pt\'e1\u269\'3fek collaborated with Jones. what is called familial advanced sleep-phase syndrome (FASPS)\'97or very early risers\'97and has found almost 90 families.{\rtlch\ltrch\dbch\hich\i\loch\i  Novel players in presynaptic vesicle trafficking.} To identify mutatio
ns in novel genes as well as genes that have previously been implicated in SV trafficking, we used the eyeless-FLP/FRT system to carry out four chemical mutagenesis screens. with apparent normal eye morphology (300,000 flies) for their ability to phototax 
(retained 10,000).}
\par \pard\plain \ltrpar\s1\sl276\slmult1{\*\hyphen2\hyphlead2\hyphtrail2\hyphmax0}\sa200\ql\rtlch\af7\afs22\lang1025\ltrch\dbch\af6\langfe1033\hich\f1\fs22\lang1033\loch\f1\fs22\lang1033{\rtlch \ltrch\loch\f1\fs22\lang1033\i0\b0{\ltrch\dbch\hich\b\loch\b Lots of Greek letters and symbols: }}{\rtlch \ltrch\loch\f1\fs22\lang1033\i0\b0{\rtlch\ltrch\dbch\hich\b\loch\b \line }The combined incidence of \u945\'3f and \u954\'3f and \u946\'3f and \u966\'3f and \u8805\'3f and d\'e9tected \'b5m and \'b1 and \'e1 and \'e3 and \'fc and \'89 and \'97 and \'a9 and \'85 and \u948\'3f and \u955\'3f and \u954\'3f and de novo rearrangements that are mediated by segmental duplications is estimated at
 1/1,000 live births. \u8592\'3f arrows \u8594\'3f fraction \u8541\'3f symbol \u8805\'3f This includes 3 percent of ~130 regions of the human genome that we believe show a predilection\'96to\'96segmental\'96aneusomy.}
\par \pard\plain \ltrpar\s1\sl276\slmult1{\*\hyphen2\hyphlead2\hyphtrail2\hyphmax0}\sa200\ql\rtlch\af7\afs22\lang1025\ltrch\dbch\af6\langfe1033\hich\f1\fs22\lang1033\loch\f1\fs22\lang1033 {\rtlch \ltrch\loch\f1\fs22\lang1033\i0\b0 These are {\ltrch\dbch\hich\b\loch\b accented letters}:  \u971\'3f \u972\'3f \'eb \'e9 \'e8 \'e5 \u283\'3f}
\par \pard\plain \ltrpar\s1\sl276\slmult1{\*\hyphen2\hyphlead2\hyphtrail2\hyphmax0}\sa200\ql\rtlch\af7\afs22\lang1025\ltrch\dbch\af6\langfe1033\hich\f1\fs22\lang1033\loch\f1\fs22\lang1033{\rtlch \ltrch\loch\f1\fs22\lang1033\i0\b0{\ltrch\dbch\hich\b\loch\b Hyperlinks:}}{\rtlch \ltrch\loch\f1\fs22\lang1033\i0\b0  In collaboration with the laboratories of {\field{\*\fldinst HYPERLINK "http://www.hhmi.org/research/investigators/spradling.html" }{\fldrslt \*\cs13\cf2\ul\ulc0\rtlch\ltrch\dbch\hich\f1\fs22\lang1033\loch\f1\fs22\lang1033 Allan Spradling}} (HHMI, Carnegie Institution of Washington), Roger Hoskins (Lawrence Berkeley National Laboratory), and {\field{\*\fldinst HYPERLINK "http://www.hhmi.org/research/groupleaders/rubin.html" }{\fldrslt \*\cs13\cf2\ul\ulc0\rtlch\ltrch\dbch\hich\f1\fs22\lang1033\loch\f1\fs22\lang1033 Gerald Rubin}} via \u934\'3fC31-mediated integration ({\field{\*\fldinst HYPERLINK "http://flypush.imgen.bcm.tmc.edu/lab/pacman.html" }{\fldrslt \*\cs13\cf2\ul\ulc0\rtlch\ltrch\dbch\hich\f1\fs22\lang1033\loch\f1\fs22\lang1033 http://flypush.imgen.bcm.tmc.edu/lab/pa
cman.html}}).}
\par \pard\plain \ltrpar\s1\sl276\slmult1{\*\hyphen2\hyphlead2\hyphtrail2\hyphmax0}\sa200\ql\rtlch\af7\afs22\lang1025\ltrch\dbch\af6\langfe1033\hich\f1\fs22\lang1033\loch\f1\fs22\lang1033{\rtlch \ltrch\loch\f1\fs22\lang1033\i0\b0\ltrch\dbch\hich\b\loch\b Pamela J. Bj\'f6rkman, Ph.D.}
\par \pard\plain \ltrpar\s1\sl276\slmult1{\*\hyphen2\hyphlead2\hyphtrail2\hyphmax0}\sa200\ql\rtlch\af7\afs22\lang1025\ltrch\dbch\af6\langfe1033\hich\f1\fs22\lang1033\loch\f1\fs22\lang1033{\rtlch \ltrch\loch\f1\fs22\lang1033\i0\b0{\ltrch\dbch\hich\b\loch\b Subscripts and superscripts:}}{\rtlch \ltrch\loch\f1\fs22\lang1033\i0\b0  the polymeric immunoglobulin receptor (CO{{\*\updnprop5801}\dn9 2}), which CO{{\*\updnprop5801}\up9 2} transports polymeric antibodies into secretions, and gE-gI, a viral Fc receptor for IgG. H{{\*\updnprop5801}\dn9 2}O is not H{{\*\updnprop5801}\up9 2}O  or V{{\*\updnprop5801}\dn9 0}.}
\par \pard\plain \ltrpar\s1\sl276\slmult1{\*\hyphen2\hyphlead2\hyphtrail2\hyphmax0}\sa200\ql\rtlch\af7\afs22\lang1025\ltrch\dbch\af6\langfe1033\hich\f1\fs22\lang1033\loch\f1\fs22\lang1033 
\par \pard\plain \ltrpar\s1\sl276\slmult1{\*\hyphen2\hyphlead2\hyphtrail2\hyphmax0}\sa200\ql\rtlch\af7\afs22\lang1025\ltrch\dbch\af6\langfe1033\hich\f1\fs22\lang1033\loch\f1\fs22\lang1033{\rtlch \ltrch\loch\f1\fs22\lang1033\i0\b0\ltrch\dbch\hich\b\loch\b Bulleted list:}
\par \pard\plain \ltrpar\s1\sl276\slmult1{\*\hyphen2\hyphlead2\hyphtrail2\hyphmax0}\sa200\ql\rtlch\af7\afs22\lang1025\ltrch\dbch\af6\langfe1033\hich\f1\fs22\lang1033\loch\f1\fs22\lang1033{\rtlch \ltrch\loch\f1\fs22\lang1033\i0\b0{\rtlch\ltrch\dbch\hich\b\loch\b In Vitro Reconstitution of Ca}}{\rtlch \ltrch\loch\f1\fs22\lang1033\i0\b0{{\*\updnprop5801}\up9\rtlch\ltrch\dbch\hich\b\loch\b 2+}{\rtlch\ltrch\dbch\hich\b\loch\b -Triggered Synaptic Vesicle Fusion}}
\par \pard\plain {\listtext\pard\plain \li1440\ri0\lin1440\rin0\fi-360 \u61623\'3f\tab}\ilvl0 \ltrpar\s7\sl276\slmult1{\*\hyphen2\hyphlead2\hyphtrail2\hyphmax0}\ls0\li1440\ri0\lin1440\rin0\fi-360\sa200\ql\rtlch\af7\afs22\lang1025\ltrch\dbch\af6\langfe1033\hich\f1\fs22\lang1033\loch\f1\fs22\lang1033 {\rtlch \ltrch\loch\f1\fs22\lang1033\i0\b0 CNTs bind with high specificity }
\par \pard\plain {\listtext\pard\plain \li1440\ri0\lin1440\rin0\fi-360 \u61623\'3f\tab}\ilvl0 \ltrpar\s7\sl276\slmult1{\*\hyphen2\hyphlead2\hyphtrail2\hyphmax0}\ls0\li1440\ri0\lin1440\rin0\fi-360\sa200\ql\rtlch\af7\afs22\lang1025\ltrch\dbch\af6\langfe1033\hich\f1\fs22\lang1033\loch\f1\fs22\lang1033 {\rtlch \ltrch\loch\f1\fs22\lang1033\i0\b0 at neuromuscular junctions }
\par \pard\plain {\listtext\pard\plain \li1440\ri0\lin1440\rin0\fi-360 \u61623\'3f\tab}\ilvl0 \ltrpar\s7\sl276\slmult1{\*\hyphen2\hyphlead2\hyphtrail2\hyphmax0}\ls0\li1440\ri0\lin1440\rin0\fi-360\sa200\ql\rtlch\af7\afs22\lang1025\ltrch\dbch\af6\langfe1033\hich\f1\fs22\lang1033\loch\f1\fs22\lang1033 {\rtlch \ltrch\loch\f1\fs22\lang1033\i0\b0 The molecular details of the toxin-cell }
\par \pard\plain {\listtext\pard\plain \li1440\ri0\lin1440\rin0\fi-360 \u61623\'3f\tab}\ilvl0 \ltrpar\s7\sl276\slmult1{\*\hyphen2\hyphlead2\hyphtrail2\hyphmax0}\ls0\li1440\ri0\lin1440\rin0\fi-360\sa200\ql\rtlch\af7\afs22\lang1025\ltrch\dbch\af6\langfe1033\hich\f1\fs22\lang1033\loch\f1\fs22\lang1033 {\rtlch \ltrch\loch\f1\fs22\lang1033\i0\b0 recognition has been elusive }
\par \pard\plain {\listtext\pard\plain \li1440\ri0\lin1440\rin0\fi-360 \u61623\'3f\tab}\ilvl0 \ltrpar\s7\sl276\slmult1{\*\hyphen2\hyphlead2\hyphtrail2\hyphmax0}\ls0\li1440\ri0\lin1440\rin0\fi-360\sa200\ql\rtlch\af7\afs22\lang1025\ltrch\dbch\af6\langfe1033\hich\f1\fs22\lang1033\loch\f1\fs22\lang1033 {\rtlch \ltrch\loch\f1\fs22\lang1033\i0\b0 determined at 2.15-\'c5 resolution}
\par \pard\plain \ltrpar\s1\sl276\slmult1{\*\hyphen2\hyphlead2\hyphtrail2\hyphmax0}\sa200\ql\rtlch\af7\afs22\lang1025\ltrch\dbch\af6\langfe1033\hich\f1\fs22\lang1033\loch\f1\fs22\lang1033 {\rtlch \ltrch\loch\f1\fs22\lang1033\i0\b0 The 6.7-\'c5 map of the {\rtlch\ltrch\dbch\hich\i\loch\i Escherichia coli} is actually visible as "bumps." Both \u945\'3f-helices and \u946\'3f-sheets}
\par \pard\plain \ltrpar\s1\sl276\slmult1{\*\hyphen2\hyphlead2\hyphtrail2\hyphmax0}\sa200\ql\rtlch\af7\afs22\lang1025\ltrch\dbch\af6\langfe1033\hich\f1\fs22\lang1033\loch\f1\fs22\lang1033 
\par }""")


doc = Rtf15Reader.read(content)

import xhtml
print xhtml.docTemplate % XHTMLWriter.write(doc).getvalue()
