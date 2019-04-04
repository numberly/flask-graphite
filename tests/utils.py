import pytest

from flask_graphite.utils import get_request_metric_prefix

uri_to_metric = {
    "/test": {
        "url_rule": "test",
        "path": "test"
    },
    "/foo/bar": {
        "url_rule": "foo|bar",
        "path": "foo|bar"
    },
    "/foo/bar/42": {
        "url_rule": "foo|bar|baz",
        "path": "foo|bar|42"
    }
}


@pytest.fixture
def routed_app(app):
    @app.route("/test")
    @app.route("/foo/bar")
    @app.route("/foo/bar/<int:baz>")
    def view(baz=None):
        return baz
    return app


@pytest.mark.parametrize("uri,metric", list(uri_to_metric.items()))
def test_get_request_metric_prefix(routed_app, uri, metric):
    with routed_app.test_request_context(uri):
        assert get_request_metric_prefix() == metric["url_rule"]


@pytest.mark.parametrize("uri,metric", list(uri_to_metric.items()))
def test_get_request_metric_prefix_with_path(routed_app, uri, metric):
    routed_app.config["FLASK_GRAPHITE_METRIC_TEMPLATE"] = "path"
    with routed_app.test_request_context(uri):
        assert get_request_metric_prefix() == metric["path"]
