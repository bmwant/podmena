import os
from unittest.mock import patch

from podmena import cli, config

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


@patch("click.confirm")
@patch("podmena.cli._info")
@patch("podmena.cli.check_exists")
@patch("podmena.cli.force_symlink")
@patch("podmena.cli.set_git_global_hooks_path")
def test_global_install(
    set_git_global_hooks_path_mock,
    force_symlink_mock,
    check_exists_mock,
    info_mock,
    confirm_mock,
    runner,
):
    check_exists_mock.return_value = True
    confirm_mock.return_value = True

    result = runner.invoke(cli.cli, ["install", "global"])

    assert result.exit_code == 0
    # TODO: check alert message for the info
    info_mock.assert_called_once()
    check_exists_mock.assert_called_once()
    force_symlink_mock.assert_called_once()
    set_git_global_hooks_path_mock.assert_called_once_with(config.GLOBAL_HOOKS_DIR)
    assert result.output == "✨ 🍒 ✨ Installed globally for all repositories!\n"


@patch("podmena.cli.unset_git_global_hooks_path")
def test_global_uninstall(
    unset_git_global_hooks_path_mock,
    runner,
):
    unset_git_global_hooks_path_mock.return_value = 0
    result = runner.invoke(cli.cli, ["uninstall", "global"])

    assert result.exit_code == 0
    assert result.output == "💥 🚫 💥 Deactivated podmena globally.\n"
    unset_git_global_hooks_path_mock.assert_called_once_with()


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
    assert result.output == "✨ podmena is activated for current repository.\n"


@patch("click.confirm")
@patch("podmena.cli.check_exists")
@patch("podmena.cli.get_git_root_dir")
@patch("podmena.cli.get_git_config_hooks_value")
def test_status_active_globally(
    get_git_config_hooks_value_mock,
    get_git_root_dir_mock,
    check_exists_mock,
    confirm_mock,
    runner,
):
    confirm_mock.return_value = False  # skip actual installation here
    check_exists_mock.return_value = True
    get_git_root_dir_mock.return_value = None
    get_git_config_hooks_value_mock.return_value = config.GLOBAL_HOOKS_DIR

    runner.invoke(cli.cli, ["install", "global"])
    confirm_mock.assert_called_once()

    result = runner.invoke(cli.cli, ["status"])
    get_git_root_dir_mock.assert_called_once_with()
    get_git_config_hooks_value_mock.assert_called_once_with()
    assert check_exists_mock.call_count == 2

    assert result.exit_code == 0
    assert result.output == "✨ podmena is activated globally.\n"


@patch("podmena.cli.get_git_root_dir")
@patch("podmena.cli.get_git_config_hooks_value")
def test_status_inactive(
    get_git_config_hooks_value_mock,
    get_git_root_dir_mock,
    runner,
):
    get_git_root_dir_mock.return_value = None

    result = runner.invoke(cli.cli, ["status"])
    get_git_root_dir_mock.assert_called_once_with()
    get_git_config_hooks_value_mock.assert_called_once_with()

    assert result.exit_code == 0
    assert (
        result.output
        == "🍄 podmena is not activated neither for current repository nor globally.\n"
    )
