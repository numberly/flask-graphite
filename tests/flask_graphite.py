import pytest

from flask_graphite.flask_graphite import FlaskGraphite, logger


@pytest.fixture
def plugin():
    return FlaskGraphite()


def test_init_app(app, plugin):
    plugin.init_app(app)
    assert plugin.app is None


def test_init_failed(mocker, app, plugin):
    mocker.patch.object(logger, "error")
    app.config["FLASK_GRAPHITE_CARBON_DRYRUN"] = False
    plugin.init_app(app)
    assert logger.error.called


def test_instance_with_app(app):
    plugin = FlaskGraphite(app)
    assert plugin.app is app


def test_get_config(app, plugin):
    app.config["FLASK_GRAPHITE_CARBON_HOST"] = "localhost"
    app.config["FLASK_GRAPHITE_CARBON_PORT"] = 2023
    app.config["FLASK_GRAPHITE_CARBON_DRYRUN"] = True
    config = plugin.get_config(app)
    assert "carbon" in config
    assert config["carbon"] == {"host": "localhost", "port": 2023,
                                "dryrun": True}


def test_setup_graphitesend(app, plugin):
    app.config["FLASK_GRAPHITE_CARBON_DRYRUN"] = True
    app.config["FLASK_GRAPHITE_CARBON_AUTORECONNECT"] = True
    config = plugin.get_config(app)
    carbon_conf = config["carbon"]
    client = plugin.setup_graphitesend(carbon_conf)
    assert client.dryrun == True
    assert client._autoreconnect == True
