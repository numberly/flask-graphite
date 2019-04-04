import logging

import pytest

from flask_graphite import FlaskGraphite


@pytest.fixture
def plugin():
    return FlaskGraphite()


def test_init(app):
    FlaskGraphite(app)


def test_init_app(app, plugin):
    plugin.init_app(app)


def test_init_failed(caplog, app, plugin):
    caplog.set_level(logging.ERROR)
    app.config["FLASK_GRAPHITE_DRYRUN"] = False
    plugin.init_app(app)
    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == "ERROR"
