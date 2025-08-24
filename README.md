[![License: GPL](https://img.shields.io/badge/License-GPL-green.svg)](https://github.com/dkrajzew/db2qthelp/blob/main/LICENSE)
[![PyPI version](https://badge.fury.io/py/db2qthelp.svg)](https://pypi.org/project/db2qthelp/)
![test](https://github.com/dkrajzew/db2qthelp/actions/workflows/test.yml/badge.svg)
[![Downloads](https://static.pepy.tech/badge/db2qthelp)](https://pepy.tech/projects/db2qthelp)
[![Downloads](https://static.pepy.tech/badge/db2qthelp/week)](https://pepy.tech/projects/db2qthelp)
[![Coverage Status](https://coveralls.io/repos/github/dkrajzew/db2qthelp/badge.svg?branch=main)](https://coveralls.io/github/dkrajzew/db2qthelp?branch=main)
[![Documentation Status](https://readthedocs.org/projects/db2qthelp/badge/?version=latest)](https://db2qthelp.readthedocs.io/en/latest/?badge=latest)

__db2qthelp__ &mdash; a DocBook book to QtHelp project converter

# Introduction

__db2qthelp__ converts a [DocBook](https://docbook.org/) [book](https://tdg.docbook.org/tdg/4.5/book.html) to a [QtHelp](https://doc.qt.io/qt-5/qthelp-framework.html) project. It is written in [Python](https://www.python.org/) and started on the command line.

__db2qthelp__ is in an early stage of development. It works well for me but it may work with my setup only. I try to make it usable nonetheless, so let me know if something does not work. Thanks.


# Usage

Given that your [xsltproc](https://gitlab.gnome.org/GNOME/libxslt) together with your [DocBook](https://docbook.org/) look-up paths are set up and that the [Qt](https://www.qt.io/) applications needed to build [Qt](https://www.qt.io/) Help files are in your executable path, you may convert your [DocBook](https://docbook.org/) book into [Qt](https://www.qt.io/) Help files like this:

```console
db2qthelp.py -i userdocs.xml
```

That&#39;s all &#x1F603;. You&#39;ll get a .qch and a .qhc file you may use directly in your [Qt](https://www.qt.io/) Help widget&#8230;

## Options

The script has the following options:

* **--config *&lt;FILE&gt;*** / **-c *&lt;FILE&gt;***: Reads the named configuration file
* **--input *&lt;INPUT&gt;*** / **-i *&lt;INPUT&gt;***: Defines the DocBook HTML document to parse
* **--destination *&lt;DESTINATION&gt;* / **-d *&lt;DESTINATION&gt;***: Sets the output folder
* **--appname *&lt;APPNAME&gt;*** / **-a *&lt;APPNAME&gt;***: Sets the name of the application
* **--css-definition *&lt;CSS_DEFINITION&gt;***: Defines the CSS definition file to use
* **--generate-css-definition**: If set, a CSS definition file is generated
* **--qhp-template *&lt;QHP_TEMPLATE&gt;***: Defines the QtHelp project (.qhp) template to use
* **--generate-qhp-template**: If set, a QtHelp project (.qhp) template is generated
* **--qt-path *&lt;QT_PATH&gt;*** / **-Q *&lt;QT_PATH&gt;***: Sets the path to the Qt binaries
* **--xslt-path *&lt;XSLT_PATH&gt;*** / **-X *&lt;XSLT_PATH&gt;***: Sets the path to xsltproc
* **--help** / **-h**: show this help message and exit
* **--version**: show program&#39;s version number and exit


## Examples

```shell
db2qthelp -i userdocs.xml
```

Generates Qt Help files by processing the DocBook book ```userdocs.xml```. The default CSS style sheets will applied, the used binaries are assumed to be in the path.

```shell
db2qthelp -i userdocs/ --css-definition my_style.css
```

Will collect the HTML files located in the folder ```userdocs```, apply the CSS located in ```my_style.css```, and build the Qt Help files from all files found in the given folder.


## Documentation

* The complete documentation is located at <https://db2qthelp.readthedocs.io/en/latest/>
* The github repository is located at: <https://github.com/dkrajzew/db2qthelp>
* Discussions are open at <https://github.com/dkrajzew/db2qthelp/discussions>
* The issue tracker is located at: <https://github.com/dkrajzew/db2qthelp/issues>
* The PyPI page is located at: <https://pypi.org/project/db2qthelp/>
* The code documentation (pydoc) is located at: <http://www.krajzewicz.de/docs/db2qthelp.html>


## Installation

The current version is 0.4.0. You may install the latest release using pip:

```console
python -m pip install db2qthelp
```

Or download the [latest release](https://github.com/dkrajzew/db2qthelp/releases/tag/0.4.0) from github. You may as well clone or download the [db2qthelp git repository](https://github.com/dkrajzew/db2qthelp). There is also a page about [installing db2qthelp](install.md) which lists further options.


## License

**db2qthelp** is licensed under the [GPLv3 license](https://raw.githubusercontent.com/dkrajzew/db2qthelp/refs/heads/main/LICENSE).


# Examples / Users

**db2qthelp** was used to generate the in-app help for the following applications:

* [PaletteWB](https://www.palettewb.com), an MS Windows application for editing color palettes;
* [ShaderWB](https://www.krajzewicz.de/blog/shaderwb.php), an MS Windows application for developing GLSL shaders.

# ChangeLog

## db2qthelp-0.4.0 (24.08.2025)

* code
    * added support for direct processing of [DocBook](https://docbook.org/) books
    * added suport for processing chuncked [xsltproc](https://gitlab.gnome.org/GNOME/libxslt) HTML output
    * moved to argparse / configparser
    * refactoring
* deployment
    * added installation as a directly callable console script
* tests
    * added coveralls integration (![test](https://github.com/dkrajzew/db2qthelp/actions/workflows/test.yml/badge.svg))
    * improved tests (![test](https://github.com/dkrajzew/db2qthelp/actions/workflows/test.yml/badge.svg))
* docs
    * reworked documentation
    * added automatic [readthedocs](https://db2qthelp.readthedocs.io/) docs building ([![Documentation Status](https://readthedocs.org/projects/db2qthelp/badge/?version=latest)](https://db2qthelp.readthedocs.io/en/latest/?badge=latest))
* moved to GPLv3


## db2qthelp-0.2 (07.01.2023)

* Initial checkin
* Adding configuration options
* Adding a documentation
* Adding first tests


# Summary

Well, have fun. If you have any comments / ideas / issues, please submit them to [db2qthelp's issue tracker](https://github.com/dkrajzew/db2qthelp/issues) on github.


