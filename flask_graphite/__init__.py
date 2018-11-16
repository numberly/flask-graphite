# -*- coding: utf-8 -*-
import logging

from graphitesend.graphitesend import GraphiteClient, GraphiteSendException

from .request_hooks import default_hooks
from .hooks import MetricHook

logger = logging.getLogger("flask-graphite")

DEFAULT_HOST = "localhost"
DEFAULT_PORT = 2023
DEFAULT_GROUP = "flask-graphite"


class FlaskGraphite(object):
    """Register a list of hooks meant to monitor a flask application

    The configuration is read from the namespace `FLASK_GRAPHITE_` of the
    application configuration.

    The main options are:
     - FLASK_GRAPHITE_HOST: The Carbon host to send metrics
     - FLASK_GRAPHITE_PORT: The Carbon port to send metrics

    You can read :ref:`Configuring Flask-Graphite` to learn about the other
    option configurations.

    :param app: The application to monitor
    """

    def __init__(self, app=None):
        self.config = {}
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Read config and set the hooks in place to monitor the application

        :param app: The application to monitor
        """
        config = self.config[app] = app.config.get_namespace("FLASK_GRAPHITE_")
        config["graphite_server"] = config.pop("host", DEFAULT_HOST)
        config["graphite_port"] = config.pop("port", DEFAULT_PORT)
        config.setdefault("group", DEFAULT_GROUP)
        config.setdefault("autoreconnect", True)

        logger.info("config: {}".format(config))
        try:
            app.graphite = GraphiteClient(**config)
        except GraphiteSendException as e:
            logger.error("can't instanciate graphite client: {}".format(e))
        else:
            logger.info("graphite client instantiated with config: %s",
                        config)
            for hook in default_hooks:
                hook.register_into(app)
        pass

__all__ = ["FlaskGraphite", "default_hooks", "MetricHook"]
