import logging

from graphitesend.graphitesend import GraphiteClient, GraphiteSendException

logger = logging.getLogger("flask-graphite")


class FlaskGraphite(object):
    """Register a list of hooks meant to monitor a flask application

    The configuration is read from the namespace "FLASK_GRAPHITE_" of the
    application configuration.

    The main options are:
     - FLASK_GRAPHITE_CARBON_HOST: The carbon host to send metrics
     - FLASK_GRAPHITE_CARBON_PORT: The carbon port to send metrics

    All other config options starting with "FLASK_GRAPHITE_CARBON_" are passed
    without the prefix to the Graphite client at instanciation.

    :param app: The application to monitor
    """

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Initialize monitoring of the application

        :param app: The application to monitor
        """
        logger.info("configuring %s", app.name)
        self.make_config(app)
        try:
            self.setup_graphitesend()
        except GraphiteSendException:
            logger.error("Failed to setup Graphite client")
        else:
            logger.info("application %s successfully configured", app.name)

    def make_config(self, app):
        """Retrieve the configuration

        :param app: The application from which to retrieve the configuration
        """
        application_config = app.config.get_namespace("FLASK_GRAPHITE_")

        self.carbon_config = {}
        for key, value in application_config.items():
            if key.startswith("carbon_"):
                self.carbon_config[key[len("carbon_"):]] = value

    def setup_graphitesend(self):
        """Setup the graphitesend client"""
        carbon_config = self.carbon_config
        logger.debug("carbon configuration: %s", carbon_config)
        host = carbon_config.pop("host")
        port = carbon_config.pop("port")
        self.client = GraphiteClient(graphite_server=host, graphite_port=port,
                                     **carbon_config)
