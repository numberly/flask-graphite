from unittest.mock import Mock

import pytest

from flask_graphite.hooks import Hook


@pytest.fixture
def dumb_hook():
    mock = Mock()
    mock.return_value = 42
    return Hook(mock)


def test_dumb_hook_register(mocked_app, dumb_hook):
    dumb_hook.register_into(mocked_app)
    assert mocked_app.after_request.called


def test_dumb_hook_callable(dumb_hook):
    assert callable(dumb_hook)
    assert dumb_hook() == 42


def test_dumb_hook_decorator():
    @Hook
    def foo():
        pass

    assert isinstance(foo, Hook)


def test_dumb_hook_setup(mocked_app, dumb_hook):
    dumb_hook.setup(dumb_hook)
    dumb_hook.register_into(mocked_app)
    assert mocked_app.before_request.called


def test_dumb_hook_setup_decorator(mocked_app, dumb_hook):
    @dumb_hook.setup
    def foo():
        pass

    assert isinstance(foo, Hook)
