import pytest
from flask import Response

from flask_graphite.request_hooks import default_hooks, request_status_type


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


def test_status_type():
    fct = request_status_type.function
    resp = Response(None, 203)
    metric, value = fct(resp)
    assert "2XX" in metric
    resp = Response(None, 500)
    metric, value = fct(resp)
    assert "5XX" in metric
