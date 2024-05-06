from __future__ import annotations

import os
import shutil
from pathlib import Path

import docutils
import pytest
import sphinx

sample_folder = "samples"

collect_ignore = [sample_folder]


@pytest.fixture(scope="session")
def rootdir():
    return Path(__file__).parent.resolve() / sample_folder


def pytest_report_header(config):
    header = "libraries: Sphinx-%s, docutils-%s" % (
        sphinx.__display_version__,
        docutils.__version__,
    )
    if hasattr(config, "_tmp_path_factory"):
        header += "\nbase tempdir: %s" % config._tmp_path_factory.getbasetemp()

    return header


def _initialize_test_directory(session):
    if "SPHINX_TEST_TEMPDIR" in os.environ:
        tempdir = os.path.abspath(os.getenv("SPHINX_TEST_TEMPDIR"))
        print("Temporary files will be placed in %s." % tempdir)

        if os.path.exists(tempdir):
            shutil.rmtree(tempdir)

        os.makedirs(tempdir)


def pytest_sessionstart(session):
    _initialize_test_directory(session)
