from unittest.mock import Mock

from graphitesend.graphitesend import GraphiteSendException
import pytest

from flask_graphite.hooks import Hook


@pytest.fixture
def dumb_hook():
    mock = Mock()
    mock.return_value = ("foo", 42)
    mock.__name__ = "dumb"
    return Hook(mock)


def test_dumb_hook_register(mocked_app, dumb_hook):
    dumb_hook.register_into(mocked_app)
    assert mocked_app.after_request.called


def test_dumb_hook_callable(dumb_hook):
    assert callable(dumb_hook)
    assert dumb_hook() == ("foo", 42)


def test_dumb_hook_name(dumb_hook):
    assert dumb_hook.name == "dumb"


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


def test_exception_bad_type(mocked_app, dumb_hook):
    dumb_hook.type = "invalid_type"
    with pytest.raises(AttributeError):
        dumb_hook.register_into(mocked_app)


def test_application_hook(graphitesend_client, dumb_hook):
    binding = dumb_hook.bind(graphitesend_client)
    binding()
    assert graphitesend_client.send.called


def test_application_hook_failed_send(graphitesend_client, dumb_hook):
    graphitesend_client.send.side_effect = GraphiteSendException
    binding = dumb_hook.bind(graphitesend_client)
    binding()
    assert graphitesend_client.send.called
