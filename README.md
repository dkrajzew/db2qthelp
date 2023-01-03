db2qthelp &mdash; a DocBook document to Qt help pages converter

___This page is currently being built up.___

Introduction
============

__db2qthelp__ converts a DocBook document to a Qt help project.


Background
==========

I usually write my user documentation using DocBook. For my recent applications built on top of Qt, I needed something
that generates in-app help pages. __db2qthelp__ does this.


Download and Installation
=========================

The current version is [db2qthelp-0.2](https://github.com/dkrajzew/db2qthelp/releases/tag/0.2).

You may install __db2qthelp__ using

```console
python -m pip install db2qthelp
```

You may download a copy or fork the code at [db2qthelp&apos;s github page](https://github.com/dkrajzew/db2qthelp).

Besides, you may download the current release [db2qthelp-1.0](https://github.com/dkrajzew/db2qthelp/releases/tag/1.0) here:
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

* The web page is located at: http://www.krajzewicz.de/blog/db2qthelp.php
* The PyPI page is located at: https://pypi.org/project/db2qthelp/
* The github repository is located at: https://github.com/dkrajzew/db2qthelp
* The issue tracker is located at: https://github.com/dkrajzew/db2qthelp/issues


Examples / Users
================

* [PaletteWB](https://www.palettewb.com/) &mdash; a sophisticated palette editor for MS Windows.


Change Log
==========

Version 1.0
-----------

* Initial version


Summary
=======

Well, have fun. If you have any comments / ideas / issues, please submit them to [db2qthelp's issue tracker](https://github.com/dkrajzew/db2qthelp/issues) on github.

