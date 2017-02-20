from unittest.mock import Mock

from graphitesend.graphitesend import GraphiteSendException
import pytest

from flask_graphite.hooks import Hook, logger


@pytest.fixture
def dumb_hook():
    mock = Mock()
    mock.return_value = ("foo", 42)
    mock.__name__ = "dumb"
    return Hook(mock)


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


def test_dumb_hook_setup(graphitesend_client, mocked_app, dumb_hook):
    dumb_hook.setup(dumb_hook)
    dumb_hook.bind(graphitesend_client).register_into(mocked_app)
    assert mocked_app.before_request.called


def test_dumb_hook_setup_decorator(mocked_app, dumb_hook):
    @dumb_hook.setup
    def foo():
        pass

    assert isinstance(foo, Hook)


def test_exception_bad_type(mocker, mocked_app, dumb_hook,
                            graphitesend_client):
    mocker.patch.object(logger, "error")
    dumb_hook.type = "invalid_type"
    with pytest.raises(AttributeError):
        dumb_hook.bind(graphitesend_client).register_into(mocked_app)
    assert logger.error.called


def test_setup_hook_exception_bad_type(mocker, mocked_app, dumb_hook,
                                       graphitesend_client):
    @dumb_hook.setup
    def setup_hook():
        pass

    mocker.patch.object(logger, "error")
    setup_hook.type = "invalid_type"
    with pytest.raises(AttributeError):
        setup_hook.register_into(mocked_app)
    assert logger.error.called


def test_application_hook(graphitesend_client, dumb_hook):
    binding = dumb_hook.bind(graphitesend_client)
    binding(None)
    assert graphitesend_client.send.called


def test_application_hook_failed_send(mocker, graphitesend_client, dumb_hook):
    mocker.patch.object(logger, "error")
    graphitesend_client.send.side_effect = GraphiteSendException
    binding = dumb_hook.bind(graphitesend_client)
    binding(None)
    assert graphitesend_client.send.called
    assert logger.error.called


def test_application_hook_register(mocked_app, dumb_hook, graphitesend_client):
    binding = dumb_hook.bind(graphitesend_client)
    binding.register_into(mocked_app)
    assert mocked_app.after_request.called


def test_repr(dumb_hook):
    s = repr(dumb_hook)
    assert s == "Hook(dumb)"


def test_repr_application_hook(dumb_hook, graphitesend_client):
    s = repr(dumb_hook.bind(graphitesend_client))
    assert s == "ApplicationHook(Hook(dumb), {})".format(graphitesend_client)
