#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""grebakker - Utility functions for tests."""
# =============================================================================
__author__     = "Daniel Krajzewicz"
__copyright__  = "Copyright 2025, Daniel Krajzewicz"
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


# --- imports ---------------------------------------------------------------
import os
import shutil
import re
import json
import zipfile
import pathlib
import glob
from zipfile import ZipFile
TEST_PATH = os.path.split(__file__)[0]
import errno
from pathlib import Path



# --- imports ---------------------------------------------------------------
def pname(txt, path="<DIR>"):
    txt = txt.replace(str(path), "<DIR>").replace("\\", "/")
    txt = txt.replace("optional arguments", "options")
    return txt.replace("__main__.py", "db2qthelp").replace("pytest", "db2qthelp")

def tread(filepath):
    return filepath.read_text(encoding="utf-8")

#def bread(filepath):
#    return filepath.read_bytes()

def pdirtimename(txt, tmp_path):
    regex = r'([0-9]):([0-5][0-9]):([0-5][0-9])(\.[0-9]+)?'
    txt = txt.replace(str(tmp_path), "<DIR>").replace("\\", "/")
    txt = pname(txt)
    return re.sub(regex, "<DUR>", txt)

def copy_files(tmp_path, files):
    for file in files:
        if "*" not in file:
            shutil.copy(os.path.join(TEST_PATH, file), str(tmp_path / file))
            continue
        files2 = glob.glob(os.path.join(TEST_PATH, file))
        file_dir, _ = os.path.split(file)
        for file2 in files2:
            _, file2name = os.path.split(file2)
            src = os.path.join(TEST_PATH, file_dir, file2name)
            dst = tmp_path / file_dir / file2name
            shutil.copy(file2, dst)

def compare_files(tmp_path, folder, ext):
    seen = 0
    wrong = 0
    for file in os.listdir(os.path.join(tmp_path, folder)):
        if ext is not None:
            _, file_extension = os.path.splitext(file)
            if ext!=file_extension:
                continue
        orig = tread(Path(TEST_PATH) / folder / file)
        gen = tread(Path(tmp_path) / folder / file)
        if orig!=gen:
            wrong += 1 # pragma: no cover
            print(f"Mismatch for '{file}'") # pragma: no cover
            print(f"    '{Path(TEST_PATH) / folder / file}'") # pragma: no cover
            print(f"    '{Path(tmp_path) / folder / file}'") # pragma: no cover
        seen += 1
    return seen, wrong
