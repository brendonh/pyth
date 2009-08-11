from pyth.plugins.latex.writer import LatexWriter
import pythonDoc

if __name__ == "__main__":
    doc = pythonDoc.buildDoc()
    print LatexWriter.write(doc).getvalue()
