import logging
import time

from flask import request

from .hooks import Hook
from .utils import get_request_metric_prefix

logger = logging.getLogger("flask-graphite")


@Hook
def request_count(response):
    metric_prefix = get_request_metric_prefix()
    metric = metric_prefix + ".count"
    return metric, 1


@Hook
def request_status_code(response):
    status_code = response.status_code
    metric_prefix = get_request_metric_prefix()
    metric = metric_prefix + ".status_code.{}".format(status_code)
    return metric, 1


@Hook
def request_processing_time(exception):
    # shiro: before_request may not be executed, see the 4th point of
    # http://flask.pocoo.org/docs/0.10/reqcontext/#callbacks-and-errors
    if not hasattr(request, "start_time"):  # pragma: no cover
        logger.warning("request doesn't have a start_time attribute")
        return
    metric_prefix = get_request_metric_prefix()
    metric = metric_prefix + ".pt"
    return metric, time.time() - request.start_time


@request_processing_time.setup
def set_start_time():
    request.start_time = time.time()

default_hooks = [request_count, request_status_code, request_processing_time]
