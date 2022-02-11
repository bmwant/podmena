import os

import pytest
from click.testing import CliRunner

from podmena import config


def get_local_hook_path() -> str:
    return os.path.join(os.getcwd(), ".git", "hooks", config.HOOK_FILENAME)


def get_local_db_path() -> str:
    return os.path.join(os.getcwd(), ".git", "hooks", config.DATABASE_FILE)


def fake_git_repo():
    """Creates directories with a same structure as within git repository"""
    hooks_path = os.path.join(os.getcwd(), ".git", "hooks")
    os.makedirs(hooks_path)


@pytest.fixture
def runner():
    cli_runner = CliRunner()
    with cli_runner.isolated_filesystem():
        fake_git_repo()
        yield cli_runner
