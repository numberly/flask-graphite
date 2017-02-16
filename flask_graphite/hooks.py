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

    def __call__(self, *args, **kwargs):
        """Proxy for function calls"""
        return self.function(*args, **kwargs)

    @property
    def name(self):
        return self.function.__name__

    def register_into(self, obj):
        """Register the hook as a request hook in `obj`

        :param obj: Either an application or a blueprint
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


class ApplicationHook(object):
    """Binds a hook to an application's graphitesend instance

    :param hook: The hook to bind with the client
    :param client: The client to bind with the hook
    """

    def __init__(self, hook, client):
        self.hook = hook
        self.client = client

    def __call__(self, *args, **kwargs):
        send_args = self.hook(*args, **kwargs)
        try:
            self.client.send(*send_args)
        except GraphiteSendException:
            logger.error("Couldn't send metric \"%s\"", send_args)

    def register_into(self, obj):
        return self.hook.register_into(obj)
