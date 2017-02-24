import logging

from graphitesend.graphitesend import GraphiteClient, GraphiteSendException

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
        self.config[app] = app.config.get_namespace("FLASK_GRAPHITE_")
        self.config[app]["graphite_server"] = self.config[app].pop("host", None)
        self.config[app]["graphite_port"] = self.config[app].pop("port", None)

        try:
            app.graphite = GraphiteClient(**self.config[app])
        except GraphiteSendException:
            logger.error("Failed to setup Graphite client")

        for hook in default_hooks:
            hook.register_into(app)
