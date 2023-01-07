from __future__ import print_function
# ===================================================================
# db2qthelp - a DocBook book to QtHelp project converter.
# Version 0.2.
#
# Tests for the main method
#
# (c) Daniel Krajzewicz 2022-2023
# - daniel@krajzewicz.de
# - http://www.krajzewicz.de
# - https://github.com/dkrajzew/db2qthelp
# - http://www.krajzewicz.de/blog/db2qthelp.php
#
# Available under the BSD license.
# ===================================================================


# --- test functions ------------------------------------------------
def test_main_empty(capsys):
    """Test behaviour if no arguments are given"""
    import db2qthelp
    try:
        db2qthelp.main([])
        assert False
    except SystemExit as e:
        assert type(e)==type(SystemExit())
        assert e.code==2
    captured = capsys.readouterr()
    assert captured.err.replace("__main__.py", "db2qthelp.py") == """Error: no input file given (use -i <HTML_DOCBOOK>)...
Error: no application name given (use -a <APP_NAME>)...
Error: no source url given(use -s <SOURCE_URL>)...
Usage: db2qthelp.py -i <HTML_DOCBOOK> [options]+
"""
    assert captured.out == ""


def test_main_help(capsys):
    """Test behaviour when help is wished"""
    import db2qthelp
    try:
        db2qthelp.main(["--help"])
        assert False
    except SystemExit as e:
        assert type(e)==type(SystemExit())
        assert e.code==0
    captured = capsys.readouterr()
    assert captured.out.replace("__main__.py", "db2qthelp.py") == """Usage: usage:
  db2qthelp.py [options]

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -i INPUT, --input=INPUT
                        Defines the DocBook HTML document to parse
  -a APPNAME, --appname=APPNAME
                        Sets the name of the application
  -s SOURCE, --source=SOURCE
                        Sets the documentation source url
  -f FILES, --files=FILES
                        Sets the folder to collect files from
  -d DESTINATION, --destination=DESTINATION
                        Sets the output folder
  -t TEMPLATE, --template=TEMPLATE
                        Defines the QtHelp project template to use
  -g, --generate        If set, a template is generated
  -p PATH, --path=PATH  Sets the path to the Qt binaries to use
"""
    assert captured.err == ""


"""
def test_main_generate_short(capsys, tmp_path):
    import db2qthelp
    p1 = tmp_path / "template.qhp"
    try:
        db2qthelp.main(["-g"])
        assert False
    except SystemExit as e:
        assert type(e)==type(SystemExit())
        assert e.code==0
    assert p1.read_text() == db2qthelp.template
    captured = capsys.readouterr()
    assert captured.out.replace("__main__.py", "db2qthelp.py") == "Written qhp template to 'template.qhp'\n"


def test_main_generate_long(capsys, tmp_path):
    import db2qthelp
    p1 = tmp_path / "template.qhp"
    try:
        db2qthelp.main(["--generate"])
        assert False
    except SystemExit as e:
        assert type(e)==type(SystemExit())
        assert e.code==0
    assert p1.read_text() == db2qthelp.template
    captured = capsys.readouterr()
    assert captured.out.replace("__main__.py", "db2qthelp.py") == "Written qhp template to 'template.qhp'\n"
"""


def test_main_generate_alt_name_short(capsys, tmp_path):
    import db2qthelp
    p1 = tmp_path / "test.qhp"
    try:
        db2qthelp.main(["-g", "-t", p1])
        assert False
    except SystemExit as e:
        assert type(e)==type(SystemExit())
        assert e.code==0
    assert p1.read_text() == db2qthelp.template
    captured = capsys.readouterr()
    assert captured.out.replace("__main__.py", "db2qthelp.py") == "Written qhp template to '%s'\n" % p1


def test_main_generate_alt_name_long(capsys, tmp_path):
    import db2qthelp
    p1 = tmp_path / "test.qhp"
    try:
        db2qthelp.main(["--generate", "--template", p1])
        assert False
    except SystemExit as e:
        assert type(e)==type(SystemExit())
        assert e.code==0
    assert p1.read_text() == db2qthelp.template
    captured = capsys.readouterr()
    assert captured.out.replace("__main__.py", "db2qthelp.py") == "Written qhp template to '%s'\n" % p1

