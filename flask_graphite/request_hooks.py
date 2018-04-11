import logging
import time

from flask import request

from .hooks import MetricHook

logger = logging.getLogger("flask-graphite")


@MetricHook
def request_count(response):
    """Count the number of request on this route"""
    return "count", 1


@MetricHook
def request_status_code(response):
    """Count the number of requests by status code returned"""
    status_code = response.status_code
    metric = "status_code.{}".format(status_code)
    return metric, 1


@MetricHook
def request_status_type(response):
    """Count the number of requests by statys type returned (2XX, 4XX, etc)"""
    status_type = response.status_code // 100
    metric = "status_code.{}XX".format(status_type)
    return metric, 1


@MetricHook
def request_processing_time(_):
    """Measure the processing time of the of this route"""
    # shiro: before_request may not be executed, see the 4th point of
    # http://flask.pocoo.org/docs/0.10/reqcontext/#callbacks-and-errors
    if not hasattr(request, "start_time"):  # pragma: no cover
        logger.warning("request doesn't have a start_time attribute")
        return
    return "pt", time.time() - request.start_time


@request_processing_time.setup
def set_start_time():
    """setup hook for processing time (set start_time of request)"""
    request.start_time = time.time()


@MetricHook
def response_size(response):
    """Measure the size of the response body"""
    try:
        data = response.get_data()
    except RuntimeError:  # pragma: no cover
        logger.warning("Couldn't get response size")
        return
    return "size", len(data)


default_hooks = [request_count, request_status_code, request_status_type,
                 request_processing_time, response_size]

__all__ = ["request_count", "request_status_code", "request_status_type",
           "request_processing_time", "response_size", "default_hooks"]
