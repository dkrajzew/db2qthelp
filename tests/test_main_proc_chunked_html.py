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
def test_main_proc_chunked_html__1(capsys, tmp_path):
    """Generates a template using the short option"""
    os.makedirs(tmp_path / "tstdoc1_chunked_html", exist_ok=True)
    copy_files(tmp_path, ["tstdoc1_chunked_html/*.html"])
    assert compare_files(tmp_path, "tstdoc1_chunked_html", ".html")==(11, 0)
    dst_folder = str(tmp_path / "tstdoc1_chunked_html_output")
    ret = db2qthelp.main(["-i", str(tmp_path / "tstdoc1_chunked_html"), "-a", "tst1", "--destination", dst_folder])
    assert ret==0
    compare_files(tmp_path, "tstdoc1_chunked_html_output", ".qhcp")
    compare_files(tmp_path, "tstdoc1_chunked_html_output", ".qhp")
    captured = capsys.readouterr()
    assert pdirtimename(captured.out, tmp_path) == """Processing chunked HTML output from '<DIR>/tstdoc1_chunked_html'
"""
    assert captured.err == ""


