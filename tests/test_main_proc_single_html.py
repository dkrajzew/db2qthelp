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
import shutil
sys.path.append(os.path.join(os.path.split(__file__)[0], "..", "db2qthelp"))
import db2qthelp
from util import pdirtimename, copy_files, compare_files, TEST_PATH


# --- test functions ------------------------------------------------
def test_main_proc_single_html__1(capsys, tmp_path):
    """Generates a template using the short option"""
    copy_files(tmp_path, ["tstdoc1.html"])
    dst_folder = str(tmp_path / "tstdoc1_single_html")
    ret = db2qthelp.main(["-i", str(tmp_path / "tstdoc1.html"), "-a", "tst1", "--destination", dst_folder])
    assert ret==0
    captured = capsys.readouterr()
    assert pdirtimename(captured.out, tmp_path) == """Processing single HTML output from '<DIR>/tstdoc1.html'
"""
    assert captured.err == ""
    assert compare_files(tmp_path, "tstdoc1_single_html", ".html")==(11, 0)
    assert compare_files(tmp_path, "tstdoc1_single_html", ".qhcp")==(1, 0)
    assert compare_files(tmp_path, "tstdoc1_single_html", ".qhp")==(1, 0)


def test_main_proc_single_html__2(capsys, tmp_path):
    """Generates a template using the short option"""
    os.makedirs(tmp_path / "images")
    copy_files(tmp_path, ["tstdoc2.html"])
    copy_files(tmp_path / "images", ["img1.gif", "img2.gif"])
    dst_folder = str(tmp_path / "tstdoc2_single_html")
    ret = db2qthelp.main(["-i", str(tmp_path / "tstdoc2.html"), "-a", "tst2", "--destination", dst_folder])
    assert ret==0
    captured = capsys.readouterr()
    assert pdirtimename(captured.out, tmp_path) == """Processing single HTML output from '<DIR>/tstdoc2.html'
"""
    assert captured.err == ""
    assert compare_files(tmp_path, "tstdoc2_single_html", ".html")==(2, 0)
    assert compare_files(tmp_path, "tstdoc2_single_html", ".qhcp")==(1, 0)
    assert compare_files(tmp_path, "tstdoc2_single_html", ".qhp")==(1, 0)
    assert compare_files(tmp_path, "tstdoc2_single_html", ".gif")==(2, 0)


def test_main_proc_single_html__3(capsys, tmp_path):
    """Generates a template using the short option"""
    os.makedirs(tmp_path / "images")
    copy_files(tmp_path, ["tstdoc3.html"])
    copy_files(tmp_path / "images", ["img1.gif", "img2.gif"])
    dst_folder = str(tmp_path / "tstdoc3_single_html")
    ret = db2qthelp.main(["-i", str(tmp_path / "tstdoc3.html"), "-a", "tst3", "--destination", dst_folder])
    assert ret==0
    captured = capsys.readouterr()
    assert pdirtimename(captured.out, tmp_path) == """Processing single HTML output from '<DIR>/tstdoc3.html'
"""
    assert captured.err == ""
    assert compare_files(tmp_path, "tstdoc3_single_html", ".html")==(2, 0)
    assert compare_files(tmp_path, "tstdoc3_single_html", ".qhcp")==(1, 0)
    assert compare_files(tmp_path, "tstdoc3_single_html", ".qhp")==(1, 0)
    assert compare_files(tmp_path, "tstdoc3_single_html", ".gif")==(2, 0)


def test_main_proc_single_html__4(capsys, tmp_path):
    """Generates a template using the short option"""
    os.makedirs(tmp_path / "images")
    copy_files(tmp_path, ["tstdoc4.html"])
    copy_files(tmp_path / "images", ["img1.gif", "img2.gif"])
    dst_folder = str(tmp_path / "tstdoc4_single_html")
    ret = db2qthelp.main(["-i", str(tmp_path / "tstdoc4.html"), "-a", "tst4", "--destination", dst_folder])
    assert ret==0
    captured = capsys.readouterr()
    assert pdirtimename(captured.out, tmp_path) == """Processing single HTML output from '<DIR>/tstdoc4.html'
"""
    assert captured.err == ""
    assert compare_files(tmp_path, "tstdoc4_single_html", ".html")==(3, 0)
    assert compare_files(tmp_path, "tstdoc4_single_html", ".qhcp")==(1, 0)
    assert compare_files(tmp_path, "tstdoc4_single_html", ".qhp")==(1, 0)
    assert compare_files(tmp_path, "tstdoc4_single_html", ".gif")==(2, 0)

