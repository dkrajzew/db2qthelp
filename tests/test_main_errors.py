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
from util import pname, copy_files, pdirtimename


# --- test functions ------------------------------------------------
def test_main_errors__missing_input(capsys, tmp_path):
    """Generates a template using the short option"""
    try:
        db2qthelp.main(["-i", "foo.xml"])
        assert False # pragma: no cover
    except SystemExit as e:
        assert type(e)==type(SystemExit())
        assert e.code==2
    captured = capsys.readouterr()
    assert captured.out == ""
    assert pname(captured.err) == """db2qthelp: error: did not find input 'foo.xml'
"""

def test_main_errors__missing_qhp_template(capsys, tmp_path):
    """Generates a template using the short option"""
    copy_files(tmp_path, ["tstdoc1.xml"])
    try:
        db2qthelp.main(["-i", str(tmp_path / "tstdoc1.xml"), "--qhp-template", "foo.qhp"])
        assert False # pragma: no cover
    except SystemExit as e:
        assert type(e)==type(SystemExit())
        assert e.code==2
    captured = capsys.readouterr()
    assert captured.out == ""
    assert pname(captured.err) == """db2qthelp: error: did not find QtHelp project (.qhp) template file 'foo.qhp'; you may generate one using the option --generate-qhp-template
"""

def test_main_errors__missing_css_definition(capsys, tmp_path):
    """Generates a template using the short option"""
    copy_files(tmp_path, ["tstdoc1.xml"])
    try:
        db2qthelp.main(["-i", str(tmp_path / "tstdoc1.xml"), "--css-definition", "foo.css"])
        assert False # pragma: no cover
    except SystemExit as e:
        assert type(e)==type(SystemExit())
        assert e.code==2
    captured = capsys.readouterr()
    assert captured.out == ""
    assert pname(captured.err) == """db2qthelp: error: did not find CSS definition file 'foo.css'; you may generate one using the option --generate-css-definition
"""

def test_main_errors__missing_config(capsys, tmp_path):
    """Generates a template using the short option"""
    copy_files(tmp_path, ["tstdoc1.xml"])
    try:
        db2qthelp.main(["-c", "foo.cfg"])
        assert False # pragma: no cover
    except SystemExit as e:
        assert type(e)==type(SystemExit())
        assert e.code==2
    captured = capsys.readouterr()
    assert captured.out == ""
    assert pname(captured.err) == """db2qthelp: error: configuration file 'foo.cfg' does not exist
"""

def test_main_errors__unknown_extension(capsys, tmp_path):
    """Generates a template using the short option"""
    try:
        db2qthelp.main(["-i", "foo.cfg"])
        assert False # pragma: no cover
    except SystemExit as e:
        assert type(e)==type(SystemExit())
        assert e.code==2
    captured = capsys.readouterr()
    assert captured.out == ""
    assert pname(captured.err) == """db2qthelp: error: unrecognized input extension '.cfg'
"""

def test_main_errors__no_xsltproc(capsys, tmp_path):
    """Generates a template using the short option"""
    copy_files(tmp_path, ["tstdoc1.xml"])
    dst_folder = str(tmp_path / "tmp")
    ret = db2qthelp.main(["-i", str(tmp_path / "tstdoc1.xml"), "-a", "tst", "-d", dst_folder])
    assert ret==2
    captured = capsys.readouterr()
    assert pdirtimename(captured.out, tmp_path) == """Processing docboook '<DIR>/tstdoc1.xml'
... generating chunked HTML
"""
    assert captured.err == """db2qthelp: error: could not invoke xsltproc...
"""

