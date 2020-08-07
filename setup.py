from __future__ import absolute_import
from setuptools import setup, find_packages

setup(name="pyth3",
      version="0.7",
      packages = find_packages(),
      zip_safe = False,

      description="Python text markup and conversion",
      author="Brendon Hogger",
      author_email="brendonh@gmail.com",
      url="http://github.com/prechelt/pyth",
      long_description=open('README.md').read(),
      long_description_content_type="text/markdown",

      classifiers = [
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Topic :: Office/Business",
        "Topic :: Software Development :: Libraries",
        "Topic :: Text Editors :: Word Processors",
        "Topic :: Text Processing",
        "Topic :: Text Processing :: Markup",
        "Topic :: Text Processing :: Filters",
      ],

      requires = [
          "beautifulsoup4",
          "six",
      ],
)
