import os
import sys
from unittest.mock import patch
from contextlib import contextmanager

import pytest
from click.testing import CliRunner


def fake_git_repo():
    """Creates directories with a same structure as within git repository"""
    hooks_path = os.path.join(os.getcwd(), ".git", "hooks")
    os.makedirs(hooks_path)


@pytest.fixture
def runner():
    cli_runner = CliRunner()
    with cli_runner.isolated_filesystem() as path:
        fake_git_repo()
        cli_runner.root_dir = path
        # Override global config directory
        with patch("podmena.config.GLOBAL_HOOKS_DIR", path):
            yield cli_runner


@contextmanager
def eject_module(module_name):
    module = sys.modules.pop(module_name)
    try:
        yield module
    finally:
        sys.modules[module_name] = module
