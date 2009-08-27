#!/usr/bin/env python

from distutils.core import setup

setup(name="pyth",
      version="0.1.0",
      description="Convert between different document formats",
      author="Brendon Hogger",
      author_email="brendonh@taizilla.com",
      url="http://wiki.github.com/brendonh/pyth",
      packages = ["pyth", "pyth.plugins", "pyth.plugins.latex",
                  "pyth.plugins.pdf", "pyth.plugins.plaintext",
                  "pyth.plugins.python", "pyth.plugins.rst",
                  "pyth.plugins.rtf15", "pyth.plugins.xhtml"])
