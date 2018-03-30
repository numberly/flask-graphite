import pytest

from flask_graphite.utils import get_request_metric_prefix

URI_to_metric = {
    "/test": "test",
    "/foo/bar": "foo|bar",
    "/foo/bar/42": "foo|bar|baz"
}


@pytest.fixture
def routed_app(app):
    @app.route("/test")
    @app.route("/foo/bar")
    @app.route("/foo/bar/<int:baz>")
    def view(baz=None):
        return baz
    return app


@pytest.mark.parametrize("uri,metric", list(URI_to_metric.items()))
def test_URI_to_metric_converter(routed_app, uri, metric):
    with routed_app.test_request_context(uri):
        assert get_request_metric_prefix() == metric
