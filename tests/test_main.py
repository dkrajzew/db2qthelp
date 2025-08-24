from __future__ import print_function
"""db2qthelp - main tests.
"""
# ===========================================================================
__author__     = "Daniel Krajzewicz"
__copyright__  = "Copyright 2022-2024, Daniel Krajzewicz"
__credits__    = ["Daniel Krajzewicz"]
__license__    = "GPLv3"
__version__    = "0.4.0"
__maintainer__ = "Daniel Krajzewicz"
__email__      = "daniel@krajzewicz.de"
__status__     = "Development"
# ===========================================================================
# - https://github.com/dkrajzew/db2qthelp
# - http://www.krajzewicz.de/docs/db2qthelp/index.html
# - http://www.krajzewicz.de
# ===========================================================================


# --- imports -----------------------------------------------------------------
import sys
import os
sys.path.append(os.path.join(os.path.split(__file__)[0], "..", "db2qthelp"))
import db2qthelp
from util import pname


# --- test functions ------------------------------------------------
def test_main_empty1(capsys):
    """Test behaviour if no arguments are given"""
    try:
        db2qthelp.main([])
        assert False # pragma: no cover
    except SystemExit as e:
        assert type(e)==type(SystemExit())
        assert e.code==2
    captured = capsys.readouterr()
    assert pname(captured.err) == """db2qthelp: error: no input file given (use -i <HTML_DOCBOOK>)...
"""
    assert captured.out == ""


def test_main_version(capsys):
    """Test behaviour when version information shall be printed"""
    try:
        db2qthelp.main(["--version"])
        assert False # pragma: no cover
    except SystemExit as e:
        assert type(e)==type(SystemExit())
        assert e.code==0
    captured = capsys.readouterr()
    assert pname(captured.out) == """db2qthelp 0.4.0
"""
    assert captured.err == ""


def test_main_help(capsys):
    """Test behaviour when help is wished"""
    try:
        db2qthelp.main(["--help"])
        assert False # pragma: no cover
    except SystemExit as e:
        assert type(e)==type(SystemExit())
        assert e.code==0
    captured = capsys.readouterr()
    assert pname(captured.out) == """usage: db2qthelp [-h] [-c FILE] [-i INPUT] [-d DESTINATION] [-a APPNAME]
                 [--css-definition CSS_DEFINITION] [--generate-css-definition]
                 [--qhp-template QHP_TEMPLATE] [--generate-qhp-template]
                 [-Q QT_PATH] [-X XSLT_PATH] [--version]

a DocBook book to QtHelp project converter

options:
  -h, --help            show this help message and exit
  -c FILE, --config FILE
                        Reads the named configuration file
  -i INPUT, --input INPUT
                        Defines the DocBook HTML document to parse
  -d DESTINATION, --destination DESTINATION
                        Sets the output folder
  -a APPNAME, --appname APPNAME
                        Sets the name of the application
  --css-definition CSS_DEFINITION
                        Defines the CSS definition file to use
  --generate-css-definition
                        If set, a CSS definition file is generated
  --qhp-template QHP_TEMPLATE
                        Defines the QtHelp project (.qhp) template to use
  --generate-qhp-template
                        If set, a QtHelp project (.qhp) template is generated
  -Q QT_PATH, --qt-path QT_PATH
                        Sets the path to the Qt binaries
  -X XSLT_PATH, --xslt-path XSLT_PATH
                        Sets the path to xsltproc
  --version             show program's version number and exit

(c) Daniel Krajzewicz 2022-2025
"""
    assert captured.err == ""

