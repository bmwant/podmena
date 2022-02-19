from unittest.mock import patch

from podmena import cli, config


def test_executable_invocation(runner):
    result = runner.invoke(cli.cli)

    assert result.exit_code == 0

    assert "Usage" in result.output
    assert "Commands" in result.output
    assert "Options" in result.output
    assert "podmena" in result.output


def test_version_invocation(runner):
    result = runner.invoke(cli.cli, ["--version"])

    assert result.exit_code == 0
    assert result.output.startswith("🍒 podmena, version")


def test_help_invocation(runner):
    result = runner.invoke(cli.cli, ["--help"])

    assert result.exit_code == 0
    assert "Show this message and exit" in result.output


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
