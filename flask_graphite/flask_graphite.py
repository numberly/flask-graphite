import logging
import time

from flask import request

from graphitesend.graphitesend import GraphiteClient, GraphiteSendException

logger = logging.getLogger("flask-graphite")


def set_start_time():
    request.start_time = time.time()


class FlaskGraphite(object):

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        logger.info("configuring %s", app.name)
        self.make_config(app)
        try:
            self.setup_graphitesend()
            self.setup_request_hooks(app)
        except GraphiteSendException:
            logger.error("Failed to setup Graphite client")
        else:
            logger.info("application %s successfully configured", app.name)

    def make_config(self, app, namespace=None):
        application_config = app.config.get_namespace("FLASK_GRAPHITE_")

        self.carbon_config = {}
        for key, value in application_config.items():
            if key.startswith("carbon_"):
                self.carbon_config[key[len("carbon_"):]] = value

    def setup_graphitesend(self):
        carbon_config = self.carbon_config
        logger.debug("carbon configuration: %s", carbon_config)
        host = carbon_config.pop("host")
        port = carbon_config.pop("port")
        self.client = GraphiteClient(graphite_server=host, graphite_port=port,
                                     **carbon_config)

    def setup_request_hooks(self, app):
        app.before_request(set_start_time)
