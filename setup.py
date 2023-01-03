"""setup.py

This is the setup file for 

 db2qthelp - A DocBook to QtHelp converter.

(c) Daniel Krajzewicz 2022
daniel@krajzewicz.de
https://www.krajzewicz.de

Available under the BSD License.
"""

# --- imports -------------------------------------------------------
import setuptools


# --- definitions ---------------------------------------------------
with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="db2qthelp",
  version="0.2",
  author="dkrajzew",
  author_email="d.krajzewicz@gmail.com",
  description="A DocBook to QtHelp converter",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/dkrajzew/db2qthelp",
  packages=setuptools.find_packages(),
  # see https://pypi.org/classifiers/
  classifiers=[
    "Development Status :: 4 - Beta",
    "Environment :: Console",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: BSD License",
    "Operating System :: OS Independent",
    "Intended Audience :: Developers",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Documentation",
    "Topic :: Software Development",
    "Topic :: Text Processing :: Filters",
    "Topic :: Utilities"
  ],
  python_requires='>=2.7, <4',
)

