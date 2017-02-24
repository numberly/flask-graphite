import pytest
from flask import jsonify

from flask_graphite.request_hooks import default_hooks


@pytest.fixture(params=default_hooks, ids=[x.name for x in default_hooks])
def hook(request):
    yield request.param


@pytest.fixture
def hooked_app(graphitesend_client, app, hook):
    @app.route("/foo/<int:id>/<field>")
    def view(id, field):
        return jsonify("{} => {}".format(id, field))
    hook.register_into(app, graphitesend_client)
    return app


@pytest.fixture
def hooked_client(hooked_app):
    return hooked_app.test_client()


def test_dont_modify_response(hooked_client, graphitesend_client):
    response = hooked_client.get("/foo/42/bar")
    assert graphitesend_client.send.called
