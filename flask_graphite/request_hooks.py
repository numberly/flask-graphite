import logging
import time

from flask import request

from .hooks import MetricHook

logger = logging.getLogger("flask-graphite")


@MetricHook
def request_count(response):
    return "count", 1


@MetricHook
def request_status_code(response):
    status_code = response.status_code
    metric = "status_code.{}".format(status_code)
    return metric, 1


@MetricHook
def request_processing_time(_):
    # shiro: before_request may not be executed, see the 4th point of
    # http://flask.pocoo.org/docs/0.10/reqcontext/#callbacks-and-errors
    if not hasattr(request, "start_time"):  # pragma: no cover
        logger.warning("request doesn't have a start_time attribute")
        return
    return "pt", time.time() - request.start_time


@request_processing_time.setup
def set_start_time():
    request.start_time = time.time()


@MetricHook
def response_size(response):
    data = response.get_data()
    return "size", len(data)


default_hooks = [request_count, request_status_code, request_processing_time,
                 response_size]
