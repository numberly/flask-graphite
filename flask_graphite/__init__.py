# -*- coding: utf-8 -*-
import logging

from graphitesend import GraphiteClient, GraphiteSendException

from .hooks import MetricHook
from .request_hooks import default_hooks

logger = logging.getLogger("flask-graphite")


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
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Read config and set the hooks in place to monitor the application

        :param app: The application to monitor
        """
        config = app.config.get_namespace("FLASK_GRAPHITE_")
        logger.info("config: {}".format(config))

        config["graphite_server"] = config.pop("host", "localhost")
        config["graphite_port"] = config.pop("port", 2023)
        config.setdefault("group", "flask-graphite")
        config.setdefault("autoreconnect", True)
        config.pop("metric_template", None)
        try:
            app.graphite = GraphiteClient(**config)
        except GraphiteSendException as e:
            logger.error("can't instantiate graphite client: {}".format(e))
        else:
            logger.info("graphite client instantiated with config: %s", config)
            for hook in default_hooks:
                hook.register_into(app)


__all__ = ["FlaskGraphite", "default_hooks", "MetricHook"]
