from flask import request
from werkzeug.routing import _rule_re


def get_request_metric_prefix():
    """Turn the URI of the current request into a metric

    .. warning::
       You must be inside a Flask request context to call this function.
    """
    url_template = str(request.url_rule)
    url_sanitized = _rule_re.sub("\g<static>\g<variable>", url_template)
    metric_name = url_sanitized.replace('/', '|').strip('|').rstrip('|')
    return metric_name
