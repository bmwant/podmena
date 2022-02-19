import os
from unittest.mock import patch

from podmena import cli, config

from .conftest import (
    get_local_db_path,
    get_local_hook_path,
)


def test_install_local(runner):
    result = runner.invoke(cli.install, ["local"])

    assert result.exit_code == 0
    assert result.output == "✨ 🍒 ✨ Installed for current repository!\n"

    hook_file_path = get_local_hook_path()
    assert os.path.exists(hook_file_path)

    db_file_path = get_local_db_path()
    assert os.path.exists(db_file_path)


@patch("click.confirm")
@patch("podmena.cli.info")
@patch("podmena.cli.force_symlink")
@patch("podmena.cli.set_git_global_hooks_path")
def test_install_global(
    set_git_global_hooks_path_mock,
    force_symlink_mock,
    info_mock,
    confirm_mock,
    runner,
):
    confirm_mock.return_value = True

    result = runner.invoke(cli.cli, ["install", "global"])

    assert result.exit_code == 0
    # TODO: check alert message for the info
    info_mock.assert_called_once()
    force_symlink_mock.assert_called_once()
    set_git_global_hooks_path_mock.assert_called_once_with(config.GLOBAL_HOOKS_DIR)
    assert result.output == "✨ 🍒 ✨ Installed globally for all repositories!\n"


def test_install_alias_invocation(runner):
    result_on = runner.invoke(cli.cli, ["on"])

    assert result_on.exit_code == 0
    assert "Installed" in result_on.output

    result_activate = runner.invoke(cli.cli, ["activate"])
    assert result_activate.exit_code == 0
    assert "Installed" in result_activate.output


def test_install_default_invocation(runner):
    result = runner.invoke(cli.cli, ["install"])

    # Default should be a local installation
    assert result.exit_code == 0
    assert result.output == "✨ 🍒 ✨ Installed for current repository!\n"
