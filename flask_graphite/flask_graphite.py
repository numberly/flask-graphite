import logging
import functools
import time

from flask import request
from graphitesend.graphitesend import GraphiteClient, GraphiteSendException
from werkzeug.routing import _rule_re

logger = logging.getLogger("flask-graphite")


def get_request_metric_prefix():
    url_template = str(request.url_rule)
    url_sanitized = _rule_re.sub("\g<static>\g<variable>", url_template)
    metric_name = url_sanitized.replace('/', '.').strip('.').rstrip('.')
    return metric_name


def set_start_time():
    request.start_time = time.time()


def request_processing_time(exception):
    # shiro: before_request may not be executed, see the 4th point of
    # http://flask.pocoo.org/docs/0.10/reqcontext/#callbacks-and-errors
    if not hasattr(request, "start_time"):
        logger.warning("request doesn't have a start_time attribute")

    metric_prefix = get_request_metric_prefix()
    metric = metric_prefix + ".pt"
    return metric, time.time() - request.start_time


def request_count(exception):
    metric_prefix = get_request_metric_prefix()
    metric = metric_prefix + ".count"
    return metric, 1


def request_status_code(response):
    status_code = response.status_code
    metric_prefix = get_request_metric_prefix()
    metric = metric_prefix + ".status_code.{}".format(status_code)
    return metric, 1


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

    def send_wrapped(self, metric, value):
        try:
            self.client.send(metric, value)
        except GraphiteSendException:
            logger.error("Couldn't send metric %s with value %d", metric,
                         value)

    def wrap_request_hook(self, function):
        @functools.wraps(function)
        def request_hook(exception):
            metric, value = function(exception)
            self.send_wrapped(metric, value)
        return request_hook

    def setup_request_hooks(self, app):
        app.before_request(set_start_time)
        app.teardown_request(self.wrap_request_hook(request_processing_time))
        app.teardown_request(self.wrap_request_hook(request_count))
        app.after_request(self.wrap_request_hook(request_status_code))
