import os
from unittest.mock import patch

from podmena import cli

from .conftest import (
    get_local_db_path,
    get_local_hook_path,
)


def test_executable_invocation(runner):
    result = runner.invoke(cli.cli)

    assert result.exit_code == 0

    assert "Usage" in result.output
    assert "Commands" in result.output
    assert "Options" in result.output
    assert "podmena" in result.output


def test_version_invocation(runner):
    result = runner.invoke(cli.cli, ["--version"])
    executable_name = runner.get_default_prog_name(cli.cli)

    assert result.exit_code == 0
    assert executable_name in result.output
    assert "version" in result.output


def test_help_invocation(runner):
    result = runner.invoke(cli.cli, ["--help"])

    assert result.exit_code == 0
    assert "Show this message and exit" in result.output


def test_local_install(runner):
    result = runner.invoke(cli.install, ["local"])

    assert result.exit_code == 0
    assert result.output == "✨ 🍒 ✨ Installed for current repository!\n"

    hook_file_path = get_local_hook_path()
    assert os.path.exists(hook_file_path)

    db_file_path = get_local_db_path()
    assert os.path.exists(db_file_path)


def test_local_uninstall(runner):
    result_install = runner.invoke(cli.install, ["local"])
    assert result_install.exit_code == 0

    result_uninstall = runner.invoke(cli.remove, ["local"])
    assert result_uninstall.exit_code == 0
    assert result_uninstall.output == "💥 🚫 💥 Uninstalled for current repository.\n"


def test_local_uninstall_not_installed(runner):
    result_uninstall = runner.invoke(cli.remove)  # use default invocation

    assert result_uninstall.exit_code == 1
    assert (
        result_uninstall.output
        == "🍄 podmena is not installed for current repository.\n"
    )


def test_global_install():
    pass


def test_global_uninstall():
    pass


def test_alias_invocation(runner):
    result_on = runner.invoke(cli.cli, ["on"])

    assert result_on.exit_code == 0
    assert "Installed" in result_on.output

    result_activate = runner.invoke(cli.cli, ["activate"])
    assert result_activate.exit_code == 0
    assert "Installed" in result_activate.output


def test_default_invocation(runner):
    result = runner.invoke(cli.cli, ["install"])

    # Default should be a local installation
    assert result.exit_code == 0
    assert result.output == "✨ 🍒 ✨ Installed for current repository!\n"


@patch("podmena.cli.get_git_config_hooks_value")
def test_status_active_locally(
    get_git_config_hooks_value_mock,
    runner,
):
    runner.invoke(cli.cli, ["enable"])
    with patch(
        "podmena.cli.get_git_root_dir", return_value=runner.root_dir
    ) as get_git_root_dir_mock:
        result = runner.invoke(cli.cli, ["status"])
        get_git_root_dir_mock.assert_called_once_with()

    get_git_config_hooks_value_mock.assert_called_once_with()
    assert result.exit_code == 0
    assert result.output == "podmena is activated for current repository.\n"


def test_status_active_globally(runner):
    pass


@patch("podmena.cli.get_git_root_dir")
@patch("podmena.cli.get_git_config_hooks_value")
def test_status_inactive(
    get_git_config_hooks_value_mock,
    get_git_root_dir_mock,
    runner,
):
    result = runner.invoke(cli.cli, ["status"])

    get_git_root_dir_mock.assert_called_once_with()
    get_git_config_hooks_value_mock.assert_called_once_with()

    assert result.exit_code == 0
    assert (
        result.output
        == "🍄 podmena is not activated neither for current repository nor globally.\n"
    )
