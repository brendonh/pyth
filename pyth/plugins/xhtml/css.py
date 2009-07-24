
"""
Parse a css document into a python class that can be used to apply the
style to a BeautifulSoup document.
"""

import re


class Selector(object):
    """
    Represent a css selector.

    Each subclass should implement the __call__ method that takes a
    BeautifulSoup node as argument end return True if the selector
    applies to the node.
    """

    def __call__(self, node):
        raise NotImplementedError


class ClassSelector(object):
    """
    Select nodes from there class attribute.
    """

    def __init__(self, name):
        self.name = name

    def __call__(self, node):
        return node.findParent(attrs=self.name)

    def __repr__(self):
        return ".%s" % self.name


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

    def __init__(self, source=None):
        self.rules = []
        if source:
            self.parse_css(source)

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
            declarations = self.declaration_re.findall(declarations)
            for (property, value) in declarations:
                rule.properties[property] = value
            self.rules.append(rule)

    def parse_selector(self, selector):
        if selector.startswith('.'):
            return ClassSelector(selector[1:])
        # Other kind of selectors are not implemented yet
        raise ValueError

    def get_properties(self, node):
        """
        return a dict of all the properties of a given BeautifulSoup
        node found by applying the css style.
        """
        ret = {}
        for rule in self.rules:
            if rule.selector(node):
                ret.update(rule.properties)
        return ret

    def is_bold(self, node):
        """
        convenience method equivalent to
        self.get_properties(node).get('font-weight', None) == 'bold'
        """
        properties = self.get_properties(node)
        return properties.get('font-weight') == 'bold'
