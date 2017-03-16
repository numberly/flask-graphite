==========================================
Welcome to Flask-Graphite's documentation!
==========================================


.. image:: https://img.shields.io/pypi/v/flask_graphite.svg
        :target: https://pypi.python.org/pypi/flask_graphite

.. image:: https://img.shields.io/travis/numberly/flask_graphite.svg
        :target: https://travis-ci.org/numberly/flask_graphite

.. image:: https://readthedocs.org/projects/flask-graphite/badge/?version=latest
        :target: https://flask-graphite.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

Flask-graphite is an easy-to-use monitoring plugin for Flask. It enables the
recording of separate metrics for each route of your application.


Features
========

* Send metrics to graphite for each request
* Metric name based on route of the request
* Average processing time, number of request, and stats about status code for
  each route


Example
=======

Here is a mimal template to use Flask-Graphite in a project.

.. code-block:: python

    from flask import Flask

    app = Flask(__name__)
    FlaskGraphite(app)


Summary
=======

.. toctree::
   :maxdepth: 1

   readme
   installation
   get-started
   configuration
   metrics
   reference
   contributing
   history

You can also go to the :ref:`search` for a quick look at something specific.
