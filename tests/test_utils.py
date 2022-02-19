import os
import tempfile
from unittest.mock import patch

from podmena.utils import safe_delete

from .conftest import eject_module


def test_safe_delete():
    _, target_filepath = tempfile.mkstemp()

    assert os.path.exists(target_filepath)
    safe_delete(target_filepath)
    assert not os.path.exists(target_filepath)


def test_safe_delete_missing_file():
    tmp_dir = tempfile.gettempdir()
    fake_filepath = os.path.join(tmp_dir, "does_not_exist")

    assert not os.path.exists(fake_filepath)
    result = safe_delete(fake_filepath)
    # TODO: check for logger invocation once added
    assert result is None


@patch("podmena.utils.initialize")
def test_initialize_invoked_on_command(
    initialize_mock,
    runner,
):
    with eject_module("podmena"):
        from podmena import cli

        result = runner.invoke(cli.cli)
        assert result.exit_code == 0

        initialize_mock.assert_called_once_with()


@patch("podmena.utils.initialize")
def test_initialize_invoked_on_import(initialize_mock):
    with eject_module("podmena"):
        import podmena

        assert podmena.initialize is initialize_mock
        initialize_mock.assert_called_once_with()
