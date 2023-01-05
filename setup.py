# ===================================================================
# db2qthelp - a DocBook book to QtHelp project converter.
# Version 0.2.
#
# Project setup script
#
# (c) Daniel Krajzewicz 2022-2023
# - daniel@krajzewicz.de
# - http://www.krajzewicz.de
# - https://github.com/dkrajzew/db2qthelp
# - http://www.krajzewicz.de/blog/db2qthelp.php
# 
# Available under the BSD license.
# ===================================================================

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
  description="A DocBook book to QtHelp converter",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/dkrajzew/db2qthelp",
  packages=setuptools.find_packages(),
  # see https://pypi.org/classifiers/
  classifiers=[
    "Development Status :: 2 - Pre-Alpha",
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

