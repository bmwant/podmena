import os

from click.testing import CliRunner

from podmena.cli import install
from podmena.cli import HOOK_FILENAME, DATABASE_FILE


def test_local_install():
    runner = CliRunner()
    result = runner.invoke(install, ["local"])

    assert result.exit_code == 0
    assert result.output == "Successfully installed for current repository!\n"

    hook_file_path = os.path.join(
        os.getcwd(),
        ".git",
        "hooks",
        HOOK_FILENAME,
    )
    assert os.path.exists(hook_file_path)

    db_file_path = os.path.join(os.getcwd(), ".git", "hooks", DATABASE_FILE)
    assert os.path.exists(db_file_path)


def test_global_install():
    pass
