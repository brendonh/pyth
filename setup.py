from __future__ import absolute_import
from setuptools import setup, find_packages

setup(name="pyth",
      version="0.7.dev77",
      packages = find_packages(),
      zip_safe = False,

      description="Python text markup and conversion",
      author="Brendon Hogger",
      author_email="brendonh@gmail.com",
      url="http://wiki.github.com/brendonh/pyth",
      long_description=open('README').read(),

      classifiers = [
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.5",
        "Programming Language :: Python :: 2.6",
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
        "six",
      ],
)
