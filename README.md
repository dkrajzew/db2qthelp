[![License: BSD](https://img.shields.io/badge/License-BSD-green.svg)](https://github.com/dkrajzew/db2qthelp/blob/master/LICENSE) 
[![PyPI version](https://badge.fury.io/py/db2qthelp.svg)](https://pypi.python.org/pypi/db2qthelp)
[![Downloads](https://pepy.tech/badge/db2qthelp)](https://pepy.tech/project/db2qthelp)


db2qthelp &mdash; a DocBook book to QtHelp project converter

Introduction
============

__db2qthelp__ converts a DocBook book to a QtHelp project.

__db2qthelp__ is in an early stage of "development". It works well for me but it may work with my setup only.

Any feedback is appreciated.


Background
==========

I usually write my user documentation using DocBook. For my recent applications built on top of Qt, I needed something
that generates in-app help pages. __db2qthelp__ does this.


Download and Installation
=========================

The __current version__ is [db2qthelp-0.2](https://github.com/dkrajzew/db2qthelp/releases/tag/0.2).

You may __install db2qthelp__ using

```console
python -m pip install db2qthelp
```

You may __download a copy or fork the code__ at [db2qthelp&apos;s github page](https://github.com/dkrajzew/db2qthelp).

Besides, you may __download the current release__ here:
* [db2qthelp-0.2.zip](https://github.com/dkrajzew/db2qthelp/archive/refs/tags/0.2.zip)
* [db2qthelp-0.2.tar.gz](https://github.com/dkrajzew/db2qthelp/archive/refs/tags/0.2.tar.gz)


License
=======

__db2qthelp__ is licensed under the [BSD license](LICENSE).


Documentation
=============

Usage
-----

__db2qthelp__ is implemented in [Python](https://www.python.org/). It is started on the command line.

__db2qthelp__ parses a single-file HTML representation of a DocBook book. If you have a DocBook book you have 
to convert it to a single-file HTML document. The images you use within the book should be located in folders.

As soon as you have converted your DocBook book into a single-file HTML page, you may run __db2qthelp__ to
convert it into a QtHelp project.


The option 

Options
-------

The script has the following options:
* __--input/-i _&lt;PATH&gt;___: the file or the folder to process
* __--help__: Prints the help screen

Examples
--------

```console
db2qthelp -i my_page.html -a quotes.german
```

Replaces !!!

```console
db2qthelp -i my_folder -r --no-backup
```

Applies !!!


Further Documentation
---------------------

* The PyPI page is located at: https://pypi.org/project/db2qthelp/
* The github repository is located at: https://github.com/dkrajzew/db2qthelp
* The issue tracker is located at: https://github.com/dkrajzew/db2qthelp/issues


Examples / Users
================

* [PaletteWB](https://www.palettewb.com/) &mdash; a sophisticated palette editor for MS Windows.


Change Log
==========

Version 0.2
-----------

* Initial checkin
* Adding configuration options


Summary
=======

Well, have fun. If you have any comments / ideas / issues, please submit them to [db2qthelp's issue tracker](https://github.com/dkrajzew/db2qthelp/issues) on github.


