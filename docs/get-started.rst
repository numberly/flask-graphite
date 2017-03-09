===========
Get Started
===========

Here is a mimal template to use Flask-Graphite in a project::

    from flask, Flask, jsonify
    from flask_graphite.flask_graphite import FlaskGraphite


    metric_sender = FlaskGraphite()

    app = Flask(__name__)
    app.config["FLASK_GRAPHITE_HOST"] = "localhost"
    app.config["FLASK_GRAPHITE_PORT"] = 2023

    metrics.init_app(app)


    @app.route("/")
    def foo():
        return jsonify({"foo": "bar"})


    if __name__ == "__main__":
        app.run(host="localhost", port=5000)
