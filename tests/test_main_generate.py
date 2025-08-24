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


# --- test functions ------------------------------------------------
def test_main_generate_qhp_template(capsys, tmp_path):
    """Generates a qhp template"""
    p1 = tmp_path / "test.qhp"
    try:
        db2qthelp.main(["--generate-qhp-template", "--qhp-template", str(p1)])
        assert False # pragma: no cover
    except SystemExit as e:
        assert type(e)==type(SystemExit())
        assert e.code==0
    assert p1.read_text() == db2qthelp.QHP_TEMPLATE
    captured = capsys.readouterr()
    assert captured.out.replace("__main__.py", "db2qthelp.py") == f"Written qhp template to '{str(p1)}'\n"


def test_main_generate_css_definition(capsys, tmp_path):
    """Generates a css definition"""
    p1 = tmp_path / "test.css"
    try:
        db2qthelp.main(["--generate-css-definition", "--css-definition", str(p1)])
        assert False # pragma: no cover
    except SystemExit as e:
        assert type(e)==type(SystemExit())
        assert e.code==0
    assert p1.read_text() == db2qthelp.CSS_DEFINITION
    captured = capsys.readouterr()
    assert captured.out.replace("__main__.py", "db2qthelp.py") == f"Written css definition to '{str(p1)}'\n"

