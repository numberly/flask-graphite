import logging

from flask import current_app
from graphitesend.graphitesend import GraphiteSendException

from .utils import get_request_metric_prefix

logger = logging.getLogger("flask-graphite")


class MetricHook(object):
    """Represent a hook for flask requests

    This hook decorates a function to make it a suitable Flask hook.

    The function *must* return a 2-tuple which represents a metric name and
    it's value.

    :param function: The function used as hook
    :param type: The type of hook (before_request, after_request or
                 teardown_request)
    """

    def __init__(self, function, type="after_request"):
        self.function = function
        self.setup_hook = None
        self.type = type

    def __call__(self, response_or_exception=None):
        """Proxy the call to the decorated function

        :param response_or_exception: The argument passed by flask (either
        a Response object or an exception)
        """
        function_args = []
        if not self.is_setup_hook:
            function_args.append(response_or_exception)
        graphite_args = self.function(*function_args)
        if graphite_args is None:
            return response_or_exception
        metric_name, metric_value = graphite_args
        metric_name = get_request_metric_prefix() + '.' + metric_name
        try:
            current_app.graphite.send(metric_name, metric_value)
        except (RuntimeError, GraphiteSendException):  # pragma: no cover
            logger.error("Couldn't send metric \"%s\"", graphite_args)
        return response_or_exception

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, self.name)

    @property
    def name(self):
        return self.function.__name__

    __name__ = name

    @property
    def is_setup_hook(self):
        """Property to test if a hook is a setup hook"""
        return self.type == "before_request"

    def setup(self, function):
        """Mark a function as a setup hook for this hook

        A setup hook is a hook required to run before its main hook. It's
        implemented as a before_request hook.

        :param function: The function used as setup hook
        """
        self.setup_hook = MetricHook(function, type="before_request")
        return self.setup_hook

    def register_into(self, obj):
        """Register the hook as a request hook in `obj`

        Can only be used on setup hooks. Bind the hook to a client for other
        types of hooks.

        :param obj: Either an application or a blueprint
        :param client: The client to use with this hook for this application
        """
        if self.setup_hook:
            self.setup_hook.register_into(obj)
        try:
            registering_method = getattr(obj, self.type)
        except AttributeError:
            logger.error("Invalid type \"%s\". Couldn't register \"%s\" "
                         "hook into %s.", self.type, self.name, obj)
            raise
        return registering_method(self)


__all__ = ["MetricHook"]
