import logging

from graphitesend.graphitesend import GraphiteClient, GraphiteSendException

configuration_namespace = "FLASK_GRAPHITE_"
configuration_subnamespaces = ["carbon"]
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
        self.config = self.get_config(app)
        try:
            self.setup_graphitesend(self.config["carbon"])
        except GraphiteSendException:
            logger.error("Failed to setup Graphite client")
        else:
            logger.info("application %s successfully configured", app.name)

    def get_config(self, app):
        """Retrieve the configuration

        :param app: The application from which to retrieve the configuration
        """
        config = {}
        for subnamespace in configuration_subnamespaces:
            namespace = configuration_namespace + subnamespace.upper() + "_"
            config[subnamespace] = app.config.get_namespace(namespace)
        return config

    def setup_graphitesend(self, carbon_config):
        """Setup the graphitesend client"""
        logger.debug("carbon configuration: %s", carbon_config)
        host = carbon_config.pop("host")
        port = carbon_config.pop("port")
        self.client = GraphiteClient(graphite_server=host, graphite_port=port,
                                     **carbon_config)
        return self.client
