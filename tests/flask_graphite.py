import pytest

from graphitesend.graphitesend import GraphiteSendException

from flask_graphite.flask_graphite import FlaskGraphite, logger


@pytest.fixture
def plugin():
    return FlaskGraphite()


def test_init(app):
    FlaskGraphite(app)


def test_init_app(app, plugin):
    plugin.init_app(app)


def test_init_failed(mocker, app, plugin):
    mocker.patch.object(logger, "error")
    app.config["FLASK_GRAPHITE_DRYRUN"] = False
    with pytest.raises(GraphiteSendException):
        plugin.init_app(app)


def test_config(app, plugin):
    app.config["FLASK_GRAPHITE_HOST"] = "localhost"
    app.config["FLASK_GRAPHITE_PORT"] = 2023
    app.config["FLASK_GRAPHITE_DRYRUN"] = True
    plugin.init_app(app)
    assert app in plugin.config
    assert plugin.config[app] == {"graphite_server": "localhost",
                                  "graphite_port": 2023, "dryrun": True}


def test_setup_graphitesend(app, plugin):
    app.config["FLASK_GRAPHITE_DRYRUN"] = True
    app.config["FLASK_GRAPHITE_AUTORECONNECT"] = True
    plugin.init_app(app)
    assert app.graphite.dryrun is True
    assert app.graphite._autoreconnect is True
