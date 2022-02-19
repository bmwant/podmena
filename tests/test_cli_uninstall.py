from unittest.mock import patch

from podmena import cli


def test_uninstall_local(runner):
    result_install = runner.invoke(cli.install, ["local"])
    assert result_install.exit_code == 0

    result_uninstall = runner.invoke(cli.remove, ["local"])
    assert result_uninstall.exit_code == 0
    assert result_uninstall.output == "💥 🚫 💥 Uninstalled for current repository.\n"


def test_uninstall_local_not_installed(runner):
    result_uninstall = runner.invoke(cli.remove)  # use default invocation

    assert result_uninstall.exit_code == 1
    assert (
        result_uninstall.output
        == "🍄 podmena is not installed for current repository.\n"
    )


@patch("podmena.cli.unset_git_global_hooks_path")
def test_uninstall_global(
    unset_git_global_hooks_path_mock,
    runner,
):
    unset_git_global_hooks_path_mock.return_value = 0
    result = runner.invoke(cli.cli, ["uninstall", "global"])

    assert result.exit_code == 0
    assert result.output == "💥 🚫 💥 Deactivated podmena globally.\n"
    unset_git_global_hooks_path_mock.assert_called_once_with()
