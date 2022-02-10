import os
import tempfile

from podmena.utils import safe_delete


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
