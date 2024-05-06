import sys
import zipfile

import pytest
from packaging.tags import sys_tags
from .utils import build_project

CODE = """\
try:
    import coverage
except (Import Error, OSError):
    pass
else:
    coverage.process_startup()
"""


def test_build_no_options(new_project):
    print(new_project)
    build_project()
