import os

from click.testing import CliRunner

from podmena import config
from podmena.cli import install


def test_local_install():
    runner = CliRunner()
    result = runner.invoke(install, ["local"])

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
