import pytest

from flask_graphite.request_hooks import default_hooks


@pytest.fixture(params=default_hooks, ids=[x.name for x in default_hooks])
def hook(mocker, request):
    _hook = request.param
    mocker.patch.object(_hook, "function")
    _hook.function.return_value = ("foo", 1)
    yield _hook


@pytest.fixture
def plugged_client(plugged_app):
    return plugged_app.test_client()


def test_dont_modify_response(plugged_client, hook):
    plugged_client.get("/foo/42/bar")
    assert hook.function.called
