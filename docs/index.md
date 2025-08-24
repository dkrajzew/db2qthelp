[![License: GPL](https://img.shields.io/badge/License-GPL-green.svg)](https://github.com/dkrajzew/db2qthelp/blob/main/LICENSE)
[![PyPI version](https://badge.fury.io/py/db2qthelp.svg)](https://pypi.org/project/db2qthelp/)
![test](https://github.com/dkrajzew/db2qthelp/actions/workflows/test.yml/badge.svg)
[![Downloads](https://static.pepy.tech/badge/db2qthelp)](https://pepy.tech/projects/db2qthelp)
[![Downloads](https://static.pepy.tech/badge/db2qthelp/week)](https://pepy.tech/projects/db2qthelp)
[![Coverage Status](https://coveralls.io/repos/github/dkrajzew/db2qthelp/badge.svg?branch=main)](https://coveralls.io/github/dkrajzew/db2qthelp?branch=main)
[![Documentation Status](https://readthedocs.org/projects/db2qthelp/badge/?version=latest)](https://db2qthelp.readthedocs.io/en/latest/?badge=latest)
[![Dependecies](https://img.shields.io/badge/dependencies-none-green)](https://img.shields.io/badge/dependencies-none-green)

[![Donate](https://www.paypalobjects.com/en_US/i/btn/btn_donate_SM.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=GVQQWZKB6FDES)

#

__db2qthelp__ &mdash; a DocBook book to QtHelp project converter

## Introduction

__db2qthelp__ converts a [DocBook](https://docbook.org/) [book](https://tdg.docbook.org/tdg/4.5/book.html) to a [QtHelp](https://doc.qt.io/qt-5/qthelp-framework.html) project. It is written in [Python](https://www.python.org/) and started on the command line.

__db2qthelp__ is in an early stage of development. It works well for me but it may work with my setup only. I try to make it usable nonetheless, so let me know if something does not work. Thanks.

## Usage

Given that your [xsltproc](https://gitlab.gnome.org/GNOME/libxslt) together with your [DocBook](https://docbook.org/) look-up paths are set up and that the [Qt](https://www.qt.io/) applications needed to build [Qt](https://www.qt.io/) Help files are in your executable path, you may convert your [DocBook](https://docbook.org/) book into [Qt](https://www.qt.io/) Help files like this:

```console
db2qthelp.py -i userdocs.xml
```

That&#39;s all &#x1F603;. You&#39;ll get a .qch and a .qhc file you may use directly in your [Qt](https://www.qt.io/) Help widget&#8230;

## Documentation

The documentation consists of a [user manual](usage.md) and a [man-page like call documentation](cmd.md).

If you want to contribute, you may check the [API documentation](api.md) or visit [db2qthelp on github](https://github.com/dkrajzew/db2qthelp) where besides the code you may find the [db2qthelp issue tracker](https://github.com/dkrajzew/db2qthelp/issues) or a [discussions about db2qthelp](https://github.com/dkrajzew/db2qthelp/discussions) section.

Additional documentation includes a page with relevant [links](links.md) or the [ChangeLog](changes.md). You may find the complete documentation at the [db2qthelp readthedocs pages](https://db2qthelp.readthedocs.io/).


## Installation

The current version is 0.4.0. You may install the latest release using pip:

```console
python -m pip install db2qthelp
```

Or download the [latest release](https://github.com/dkrajzew/db2qthelp/releases/tag/0.4.0) from github. You may as well clone or download the [db2qthelp git repository](https://github.com/dkrajzew/db2qthelp). There is also a page about [installing db2qthelp](install.md) which lists further options.


## License

**db2qthelp** is licensed under the [GPLv3 license](license.md).


## Background

I usually write my user documentation using [DocBook](https://docbook.org/). For my recent applications built on top of [Qt](https://www.qt.io/), I needed something
that generates in-app help pages. __db2qthelp__ does this.


## Status &amp; Contributing

**db2qthelp** is in an early development stage. Yet, it is not my major project, so extensions and new versions may take some time. If you need something or have a comment, you may drop me a mail or [add an issue](https://github.com/dkrajzew/db2qthelp/issues).
