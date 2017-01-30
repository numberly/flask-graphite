import logging

from graphitesend.graphitesend import GraphiteClient

logger = logging.getLogger("flask-graphite")


class FlaskGraphite(object):

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        logger.info("configuring %s", app.name)
        self.make_config(app)
        self.setup_graphitesend()
        logger.info("application %s successfully configured")

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
