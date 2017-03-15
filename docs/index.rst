==========================================
Welcome to Flask-Graphite's documentation!
==========================================

Flask-graphite is an easy-to-use monitoring plugin for Flask. It enables the
recording of separate metrics for each route of your application.

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
