#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""db2qthelp - Setup module."""
# ===========================================================================
__author__     = "Daniel Krajzewicz"
__copyright__  = "Copyright 2022-2025, Daniel Krajzewicz"
__credits__    = ["Daniel Krajzewicz"]
__license__    = "BSD"
__version__    = "0.4"
__maintainer__ = "Daniel Krajzewicz"
__email__      = "daniel@krajzewicz.de"
__status__     = "Development"
# ===========================================================================
# - https://github.com/dkrajzew/db2qthelp
# - http://www.krajzewicz.de/docs/db2qthelp/index.html
# - http://www.krajzewicz.de
# ===========================================================================


# --- imports ---------------------------------------------------------------
import setuptools


# --- definitions -----------------------------------------------------------
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="db2qthelp",
    version="0.4",
    author="dkrajzew",
    author_email="d.krajzewicz@gmail.com",
    description="A DocBook book to QtHelp converter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='http://db2qthelp.readthedocs.org/',
    download_url='http://pypi.python.org/pypi/db2qthelp',
    project_urls={
        'Documentation': 'https://db2qthelp.readthedocs.io/',
        'Source': 'https://github.com/dkrajzew/db2qthelp',
        'Tracker': 'https://github.com/dkrajzew/db2qthelp/issues',
        'Discussions': 'https://github.com/dkrajzew/db2qthelp/discussions',
    },
    license='BSD',
    packages = [""],
    package_dir = { "": "db2qthelp", "data": "db2qthelp/data" },
    entry_points = {
        'console_scripts': [
            'db2qthelp = db2qthelp:script_run'
        ]
    },
    # see https://pypi.org/classifiers/
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Documentation",
        "Topic :: Software Development",
        "Topic :: Text Processing :: Filters",
        "Topic :: Utilities"
    ],
    python_requires='>=3, <4',
)

