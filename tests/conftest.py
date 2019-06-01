import flask
import graphitesend
import pytest

from flask_graphite import FlaskGraphite

mocked_app_methods = ["before_request", "after_request", "teardown_request"]


@pytest.fixture
def app():
    _app = flask.Flask("flask-graphite")
    _app.config["FLASK_GRAPHITE_DRYRUN"] = True
    return _app


@pytest.fixture
def plugged_app(app):
    plugin = FlaskGraphite()
    plugin.init_app(app)
    return app


@pytest.fixture
def mocked_app(mocker, plugged_app):
    for method in mocked_app_methods:
        mocker.patch.object(plugged_app, method)
    return plugged_app


@pytest.fixture
def graphitesend_client(mocker):
    client = graphitesend.GraphiteClient(dryrun=True)
    mocker.patch.object(client, "send")
    return client
