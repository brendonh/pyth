import unittest
import os.path
import glob

import pyth.document
from pyth.plugins.rtf15.reader import Rtf15Reader

class TestRtfMeta(type):
    def __new__(meta, name, bases, dict):
        fileDir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "rtfs")
        files = glob.glob(os.path.join(fileDir, "*.rtf"))

        def gen_file_test(path, name):
            def test(self):
                # Just make sure they don't crash, for now
                Rtf15Reader.read(open(path, "rb"))
            test.__name__ = "test_%s" % name
            return test

        for path in files:
            name = os.path.splitext(os.path.basename(path))[0]
            dict["test_%s" % name] = gen_file_test(path, name)
            print path, name

        return type.__new__(meta, name, bases, dict)


class TestRtfFile(unittest.TestCase):
    __metaclass__ = TestRtfMeta
    pass


class TestRtfWithImage(unittest.TestCase):

    def test_inline_png(self):
        sample_with_image = os.path.join(os.path.abspath(os.path.dirname(__file__)), "rtfs", "sample-with-image.rtf")
        with open(sample_with_image, 'rb') as rtf:
            doc = Rtf15Reader.read(rtf)
            image = next(node.content[0] for node in doc.content if isinstance(node.content[0], pyth.document.Image))
            expected = {'pngblip': True, 'picw': '20714', 'picwgoal': '750', 'pich': '12143',
                        'pichgoal': '750', 'picscaley': '100', 'picscalex': '100'}
            self.assertEquals(expected, image.properties)

class TestRtfWithNonbreakingSpaces(unittest.TestCase):

    def test_tildes_are_parsed(self):
        sample_with_tildes = os.path.join(os.path.abspath(os.path.dirname(__file__)), "rtfs", "control_chars.rtf")
        with open(sample_with_tildes, 'rb') as rtf:
            doc = Rtf15Reader.read(rtf)
            traverse_text(doc, lambda text: self.assertNotIn('~', text))


class TestNestedLists(unittest.TestCase):

    def test_when_last_item_sublist_item(self):
        """ With structures like this, both lists were getting dropped
        Start
         * 1
           * 1.1
        """
        list_bug = os.path.join(os.path.abspath(os.path.dirname(__file__)), "rtfs", "list-bug.rtf")
        with open(list_bug, 'rb') as rtf:
            doc = Rtf15Reader.read(rtf)
            text = []
            traverse_text(doc, lambda x: text.append(x))
            self.assertIn('Start', text)
            self.assertIn('1', text)
            self.assertIn('1.1', text)


class TestTextProperties(unittest.TestCase):

    def test_reads_underline(self):
        text = os.path.join(os.path.abspath(os.path.dirname(__file__)), "rtfs", "text-attributes.rtf")
        with open(text, 'rb') as rtf:
            doc = Rtf15Reader.read(rtf)
            underlined = doc.content[0].content[0]
            self.assertTrue(underlined['underline'])


def traverse_text(element, function):
    if element.__class__ == pyth.document.Text:
        map(function, element.content)
    else:
        for child in element.content:
            traverse_text(child, function)


if __name__ == '__main__':
    unittest.main()
