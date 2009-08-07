from pyth.plugins.pdf.writer import PDFWriter
import pythonDoc


if __name__ == "__main__":
    doc = pythonDoc.buildDoc()
    print PDFWriter.write(doc).getvalue()
