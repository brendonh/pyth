from __future__ import absolute_import
# -*- coding: utf-8 -*-

from pyth.plugins.rtf15.reader import Rtf15Reader
from pyth.plugins.pdf.writer import PDFWriter

doc = Rtf15Reader.read(open("../reading/sample.rtf"))


fontfile = "/usr/share/fonts/truetype/msttcorefonts/Times_New_Roman%s.ttf"

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase.pdfmetrics import registerFont, registerFontFamily
from reportlab.pdfbase.ttfonts import TTFont

registerFont(TTFont('TimesTTF', fontfile % ""))
registerFont(TTFont('TimesTTF_B', fontfile % "_Bold"))
registerFont(TTFont('TimesTTF_I', fontfile % "_Italic"))
registerFont(TTFont('TimesTTF_BI', fontfile % "_Bold_Italic"))
registerFontFamily("TimesTTF", normal="TimesTTF", bold="TimesTTF_B", italic="TimesTTF_I", boldItalic="TimesTTF_BI")

stylesheet = getSampleStyleSheet()
paragraphStyle = stylesheet['Normal']
paragraphStyle.fontName = "TimesTTF"

PDFWriter.write(doc, open("output.pdf", "wb"), paragraphStyle)
