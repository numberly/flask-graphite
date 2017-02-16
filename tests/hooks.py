from unittest.mock import Mock

import pytest

from flask_graphite.hooks import Hook


@pytest.fixture
def dumb():
    mock = Mock()
    mock.return_value = 42
    return mock


def test_hook_register(mocked_app, dumb):
    hook = Hook(dumb)
    hook.register_into(mocked_app)
    assert mocked_app.after_request.called


def test_hook_callable(dumb):
    hook = Hook(dumb)
    assert callable(hook)
    assert hook() == 42


def test_hook_decorator():
    @Hook
    def foo():
        pass

    assert isinstance(foo, Hook)
