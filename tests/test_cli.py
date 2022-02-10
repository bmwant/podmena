import os

from click.testing import CliRunner

from podmena import config
from podmena import cli


def test_executable_invocation():
    runner = CliRunner()
    result = runner.invoke(cli.cli)

    assert result.exit_code == 0

    assert "Usage" in result.output
    assert "Commands" in result.output
    assert "Options" in result.output
    assert "podmena" in result.output


def test_help_invocation():
    runner = CliRunner()
    result = runner.invoke(cli.cli, ["--help"])

    assert result.exit_code == 0
    assert "Show this message and exit" in result.output


def test_local_install():
    runner = CliRunner()
    result = runner.invoke(cli.install, ["local"])

    assert result.exit_code == 0
    assert result.output == "✨ 🍒 ✨ Installed for current repository!\n"

    hook_file_path = os.path.join(
        os.getcwd(),
        ".git",
        "hooks",
        config.HOOK_FILENAME,
    )
    assert os.path.exists(hook_file_path)

    db_file_path = os.path.join(os.getcwd(), ".git", "hooks", config.DATABASE_FILE)
    assert os.path.exists(db_file_path)


def test_local_uninstall():
    pass


def test_global_install():
    pass
