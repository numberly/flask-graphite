import logging

from graphitesend.graphitesend import GraphiteClient

from .request_hooks import default_hooks

logger = logging.getLogger("flask-graphite")


class FlaskGraphite(object):
    """Register a list of hooks meant to monitor a flask application

    The configuration is read from the namespace "FLASK_GRAPHITE_" of the
    application configuration.

    The main options are:
     - FLASK_GRAPHITE_HOST: The Carbon host to send metrics
     - FLASK_GRAPHITE_PORT: The Carbon port to send metrics

    All other config options starting with "FLASK_GRAPHITE_" are passed
    without the prefix to the Graphite client at instanciation.

    :param app: The application to monitor
    """

    def __init__(self, app=None):
        self.config = {}
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        config = self.config[app] = app.config.get_namespace("FLASK_GRAPHITE_")
        config["graphite_server"] = self.config[app].pop("host", None)
        config["graphite_port"] = self.config[app].pop("port", None)

        app.graphite = GraphiteClient(**self.config[app])
        logging.info("graphite client instantiated with config: %s",
                     self.config[app])

        for hook in default_hooks:
            hook.register_into(app)
