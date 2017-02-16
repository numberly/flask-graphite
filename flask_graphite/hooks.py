class Hook(object):
    """Represent a hook for flask requests

    A hook proxy calls to its function.

    :param function: The function used as hook
    :param type: The type of hook (before_request, after_request or
                 teardown_request)
    """

    def __init__(self, function, type="after_request"):
        self.function = function
        self.type = type

    def __call__(self, *args, **kwargs):
        """Proxy for function calls"""
        return self.function(*args, **kwargs)

    def register_into(self, obj):
        """Register the hook as a request hook in `obj`

        :param obj: Either an application or a blueprint
        """
        registering_method = getattr(obj, self.type)
        return registering_method(self.function)
