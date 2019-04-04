from flask import current_app, request
from werkzeug.routing import _rule_re


def get_request_metric_prefix():
    """Turn the URI of the current request into a metric

    .. warning::
       You must be inside a Flask request context to call this function.
    """
    metric_template = current_app.config.get("FLASK_GRAPHITE_METRIC_TEMPLATE",
                                             "url_rule")
    metric_prefix = str(getattr(request, metric_template))
    metric_prefix = _rule_re.sub(r"\g<static>\g<variable>", metric_prefix)
    metric_prefix = metric_prefix.replace('/', '|').strip('|').rstrip('|')
    return metric_prefix
