from pyth.plugins.rst.writer import RSTWriter
import pythonDoc

if __name__ == "__main__":
    doc = pythonDoc.buildDoc()
    print RSTWriter.write(doc).getvalue()
