from setuptools import setup, find_packages

setup(name="pyth",
      version="0.5",
      packages = find_packages(),
      zip_safe = False,

      description="Python text markup conversion",
      author="Brendon Hogger",
      author_email="brendonh@taizilla.com",
      url="http://wiki.github.com/brendonh/pyth",
      long_description=open('README').read(),
)
