===========
Get Started
===========

Example
-------

Here is a complete example of an application using FlaskGraphite

Write this code in a `test.py` file::

    from flask, Flask, jsonify
    from flask_graphite.flask_graphite import FlaskGraphite


    metric_sender = FlaskGraphite()

    app = Flask(__name__)
    app.config["FLASK_GRAPHITE_HOST"] = "localhost"
    app.config["FLASK_GRAPHITE_PORT"] = 2023

    metrics.init_app(app)


    @app.route("/foo")
    def foo():
        return jsonify({"test": "foo"})


    @app.route("/bar")
    def bar():
        return jsonify({"test": "bar"})


    if __name__ == "__main__":
        app.run(host="localhost", port=5000)

Run this example
----------------

To run this example, you will need to run carbon-aggregator_ in local on port
2023.

You can launch the server:

.. code-block:: console

    $ python test.py

You can then make a request to the server:

.. code-block:: console

    $ curl http://localhost:5000/

By doing this, the `foo` view will be executed, and thanks to the
Flask-Graphite plugin, a number of metrics will be available.


.. _carbon-aggregator: http://graphite.readthedocs.io/en/latest/carbon-daemons.html#carbon-aggregator-py
