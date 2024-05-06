import pytest

from pure_utils.system import execute


def test_execute(mocker):
    class FakeProcess:
        def __init__(self):
            self.stdout = b"some result"
            self.stderr = b"some error"

    run_mock = mocker.patch("pure_utils.system.run", return_value=FakeProcess())

    result, error = execute(["test", "command", "with", "arguments"])

    assert result == b"some result"
    assert error == b"some error"

    run_mock.assert_called_once_with(
        ["test", "command", "with", "arguments"], stdout=-1, stderr=-1, input=None, timeout=30
    )
