from __future__ import print_function
"""db2qthelp - main tests.
"""
# ===========================================================================
__author__     = "Daniel Krajzewicz"
__copyright__  = "Copyright 2022-2024, Daniel Krajzewicz"
__credits__    = ["Daniel Krajzewicz"]
__license__    = "BSD"
__version__    = "0.2.0"
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


# --- test functions ------------------------------------------------
def test_main_empty(capsys):
    """Test behaviour if no arguments are given"""
    try:
        db2qthelp.main([])
        assert False # pragma: no cover
    except SystemExit as e:
        assert type(e)==type(SystemExit())
        assert e.code==2
    captured = capsys.readouterr()
    assert captured.err.replace("__main__.py", "db2qthelp.py") == """db2qthelp: error: no input file given (use -i <HTML_DOCBOOK>)...
db2qthelp: error: did not find template file 'template.qhp'; you may generate one using the option -g
db2qthelp: error: no application name given (use -a <APP_NAME>)...
db2qthelp: error: no source url given (use -s <SOURCE_URL>)...
"""
    assert captured.out == ""


def test_main_help(capsys):
    """Test behaviour when help is wished"""
    try:
        db2qthelp.main(["--help"])
        assert False # pragma: no cover
    except SystemExit as e:
        assert type(e)==type(SystemExit())
        assert e.code==0
    captured = capsys.readouterr()
    assert captured.out.replace("__main__.py", "db2qthelp.py") == """usage: db2qthelp [-h] [-c FILE] [-i INPUT] [-a APPNAME] [-s SOURCE] [-f FILES]
                 [-d DESTINATION] [-t TEMPLATE] [-g] [-q QT_PATH]
                 [-x XSLT_PATH] [--version]

a DocBook book to QtHelp project converter

options:
  -h, --help            show this help message and exit
  -c FILE, --config FILE
                        Reads the named configuration file
  -i INPUT, --input INPUT
                        Defines the DocBook HTML document to parse
  -a APPNAME, --appname APPNAME
                        Sets the name of the application
  -s SOURCE, --source SOURCE
                        Sets the documentation source url
  -f FILES, --files FILES
                        Sets the folder to collect files from
  -d DESTINATION, --destination DESTINATION
                        Sets the output folder
  -t TEMPLATE, --template TEMPLATE
                        Defines the QtHelp project template to use
  -g, --generate        If set, a template is generated
  -q QT_PATH, --qt-path QT_PATH
                        Sets the path to the Qt binaries
  -x XSLT_PATH, --xslt-path XSLT_PATH
                        Sets the path to xsltproc
  --version             show program's version number and exit

(c) Daniel Krajzewicz 2022-2025
"""
    assert captured.err == ""



def test_main_generate_tpl__short(capsys, tmp_path):
    """Generates a template using the short option"""
    p1 = tmp_path / "test.qhp"
    try:
        db2qthelp.main(["-g", "-t", str(p1)])
        assert False # pragma: no cover
    except SystemExit as e:
        assert type(e)==type(SystemExit())
        assert e.code==0
    assert p1.read_text() == db2qthelp.TEMPLATE
    captured = capsys.readouterr()
    assert captured.out.replace("__main__.py", "db2qthelp.py") == "Written qhp template to '%s'\n" % p1


def test_main_generate_tpl__long(capsys, tmp_path):
    """Generates a template using the long option"""
    p1 = tmp_path / "test.qhp"
    try:
        db2qthelp.main(["--generate", "--template", str(p1)])
        assert False # pragma: no cover
    except SystemExit as e:
        assert type(e)==type(SystemExit())
        assert e.code==0
    assert p1.read_text() == db2qthelp.TEMPLATE
    captured = capsys.readouterr()
    assert captured.out.replace("__main__.py", "db2qthelp.py") == "Written qhp template to '%s'\n" % p1

