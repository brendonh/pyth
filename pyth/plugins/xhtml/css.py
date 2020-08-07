
"""
Parse a css document into a python class that can be used to apply the
style to a BeautifulSoup document.
"""
from __future__ import absolute_import

import re


class Selector(object):
    """
    Represent a css selector.

    The __call__ method takes a BeautifulSoup node as argument end
    return True if the selector applies to the node.
    """

    def __init__(self, tag=None, klass=None):
        self.tag = tag
        self.klass = klass

    def check_tag(self, node):
        return not self.tag or node.findParent(self.tag)

    def check_class(self, node):
        return not self.klass or node.findParent(attrs={'class': self.klass})

    def __call__(self, node):
        return self.check_tag(node) and self.check_class(node)

    def __repr__(self):
        tag = self.tag if self.tag else ""
        klass = ".%s" % self.klass if self.klass else ""
        return "%s%s" % (tag, klass)


class Rule(object):
    """
    Represents a css rule.

    A rule consists of a selector and a dictionary of properties.
    """

    def __init__(self, selector, properties=None):
        self.selector = selector
        self.properties = properties or {}

    def __repr__(self):
        return "%s %s" % (self.selector, self.properties)


class CSS(object):
    """
    Represents a css document
    """

    # The regular expressions used to parse the css document
    # match a rule e.g: '.imp {font-weight: bold; color: blue}'
    ruleset_re = re.compile(r'\s*(.+?)\s+\{(.*?)\}')
    # match a property declaration, e.g: 'font-weight = bold'
    declaration_re = re.compile(r'\s*(.+?):\s*(.+?)\s*?(?:;|$)')
    # match a selector
    selector_re = re.compile(r'(.*?)(?:\.(.*))?$')

    def __init__(self, source=None):
        self.rules = []
        if source:
            self.parse_css(source)

    def __repr__(self):
        return repr(self.rules)

    def parse_css(self, css):
        """
        Parse a css style sheet into the CSS object.

        For the moment this will only work for very simple css
        documents.  It works by using regular expression matching css
        syntax.  This is not bullet proof.
        """
        rulesets = self.ruleset_re.findall(css)
        for (selector, declarations) in rulesets:
            rule = Rule(self.parse_selector(selector))
            rule.properties = self.parse_declarations(declarations)
            self.rules.append(rule)

    def parse_declarations(self, declarations):
        """
        parse a css declaration list
        """
        declarations = self.declaration_re.findall(declarations)
        return dict(declarations)

    def parse_selector(self, selector):
        """
        parse a css selector
        """
        tag, klass = self.selector_re.match(selector).groups()
        return Selector(tag, klass)

    def get_properties(self, node):
        """
        return a dict of all the properties of a given BeautifulSoup
        node found by applying the css style.
        """
        ret = {}
        # Try all the rules one by one
        for rule in self.rules:
            if rule.selector(node):
                ret.update(rule.properties)
        # Also search for direct 'style' arguments in the html doc
        for style_node in node.findParents(attrs={'style': True}):
            style = style_node.get('style')
            properties = self.parse_declarations(style)
            ret.update(properties)
        return ret

    def is_bold(self, node):
        """
        convenience method equivalent to
        self.get_properties(node).get('font-weight', None) == 'bold'
        """
        properties = self.get_properties(node)
        return properties.get('font-weight') == 'bold'

    def is_italic(self, node):
        properties = self.get_properties(node)
        return properties.get('font-style') == 'italic'

    def is_sub(self, node):
        properties = self.get_properties(node)
        return properties.get('vertical-align') == 'sub'

    def is_super(self, node):
        properties = self.get_properties(node)
        return properties.get('vertical-align') == 'super'

