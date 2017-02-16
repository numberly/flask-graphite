import sys

import flask
import graphitesend.graphitesend
import pytest

sys.path.insert(0, '.')

mocked_app_methods = ["before_request", "after_request", "teardown_request"]


@pytest.fixture
def app():
    return flask.Flask("flask-graphite")


@pytest.fixture
def mocked_app(mocker, app):
    for method in mocked_app_methods:
        mocker.patch.object(app, method)
    return app


@pytest.fixture
def graphitesend_client(mocker):
    client = graphitesend.graphitesend.GraphiteClient(dryrun=True)
    mocker.patch.object(client, "send")
    return client
