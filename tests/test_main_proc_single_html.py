from __future__ import print_function
"""db2qthelp - main tests.
"""
# ===========================================================================
__author__     = "Daniel Krajzewicz"
__copyright__  = "Copyright 2022-2024, Daniel Krajzewicz"
__credits__    = ["Daniel Krajzewicz"]
__license__    = "GPLv3"
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
import shutil
sys.path.append(os.path.join(os.path.split(__file__)[0], "..", "db2qthelp"))
import db2qthelp
from util import pdirtimename, copy_files, compare_files, TEST_PATH


# --- test functions ------------------------------------------------
def test_main_proc_single_html__1(capsys, tmp_path):
    """Generates a template using the short option"""
    os.environ["PATH"] += os.pathsep + "D:\\products\\z_dev\\docbook\\libxslt-1.1.26.win32\\bin"
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


