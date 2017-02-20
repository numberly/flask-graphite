import logging

from graphitesend.graphitesend import GraphiteSendException

logger = logging.getLogger("flask-graphite")


class Hook(object):
    """Represent a hook for flask requests

    A hook proxy calls to its function.

    :param function: The function used as hook
    :param type: The type of hook (before_request, after_request or
                 teardown_request)
    """

    def __init__(self, function, type="after_request"):
        self.function = function
        self.setup_hook = None
        self.type = type

    def __call__(self, response_or_exception=None):
        """Proxy for function calls"""
        if response_or_exception is None and self.is_setup_hook:
            return self.function()
        return self.function(response_or_exception)

    def __repr__(self):
        return "Hook({})".format(self.name)

    @property
    def name(self):
        return self.function.__name__

    @property
    def is_setup_hook(self):
        return self.type == "before_request"

    def setup(self, function):
        """Mark a function as a setup hook for this hook

        A setup hook is a hook required to run before its main hook. It's
        implemented as a before_request hook.

        :param function: The function used as setup hook
        """
        self.setup_hook = Hook(function, type="before_request")
        return self.setup_hook

    def bind(self, client):
        """Bind the hook with the client

        :param client: The client to bind with the hook
        :return: An ApplicationHook instance
        """
        return ApplicationHook(self, client)

    def register_into(self, obj):
        """Register the hook as a request hook in `obj`

        Can only be used on setup hooks. Bind the hook to a client for other
        types of hooks.

        :param obj: Either an application or a blueprint
        """
        try:
            registering_method = getattr(obj, self.type)
        except AttributeError:
            logger.error("Invalid type \"%s\". Couldn't register \"%s\" "
                         "hook into %s.", self.type, self.name, obj)
            raise
        return registering_method(self)


class ApplicationHook(object):
    """Binds a hook to an application's graphitesend instance

    :param hook: The hook to bind with the client
    :param client: The client to bind with the hook
    """

    def __init__(self, hook, client):
        self.hook = hook
        self.client = client

    def __call__(self, *args):
        send_args = self.hook(*args)
        try:
            self.client.send(*send_args)
        except GraphiteSendException:
            logger.error("Couldn't send metric \"%s\"", send_args)
        if args:
            response = args[0]
            return response

    def __repr__(self):
        return "ApplicationHook({}, {})".format(self.hook, self.client)

    def register_into(self, obj):
        """Register the hook as a request hook in `obj`

        :param obj: Either an application or a blueprint
        """
        if self.hook.setup_hook:
            self.hook.setup_hook.register_into(obj)
        try:
            registering_method = getattr(obj, self.hook.type)
        except AttributeError:
            logger.error("Invalid type \"%s\". Couldn't register \"%s\" "
                         "hook into %s.", self.hook.type, self.hook.name, obj)
            raise
        return registering_method(self)
