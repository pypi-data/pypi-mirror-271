import os
from setuptools import setup, find_packages

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "etncanedge_files",
    version = "0.0.2",
    author = "Marcelo Alonso",
    author_email = "marcelohalonso@outlook.com",
    description = ("Library canedge to Linux OS."),
    license = "MIT",
    keywords = "Library canedge to Linux OS.",
    url = "http://packages.python.org/etncanedge_files",
    long_description=read('README'),
    packages=find_packages(),
    requires=['fsspec', 'mdf_iter']
)