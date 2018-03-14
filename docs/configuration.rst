==========================
Configuring Flask-Graphite
==========================

How to configure Flask-Graphite?
--------------------------------

You can configure Flask-Graphite through the Flask application's configuration.

The ``FLASK_GRAPHITE_`` namespace will be fetched from the application's
configuration and used as Flask-Graphite own configuration.

Configuration keys
------------------

Here is a succint list of the different options available, and their respective
meanings. The prefix ``FLASK_GRAPHITE_`` is removed for readability.

================= ============== ============================================================
NAME              Default        Description
================= ============== ============================================================
``HOST``          localhost      The host of the carbon-aggregator installation.
``PORT``          2023           The port of the carbon-aggregator installation.
``PREFIX``                       A prefix that will be prepended to all metrics.
``GROUP``         flask-graphite A string that will be added between the host and the actual.
                                 metric name to generate the complete metric name.
``DEBUG``                        Enable debug flag on graphitesend.
``SYSTEM_NAME``                  The name of the system which sends the metrics (hostname).
``SUFFIX``                       A suffix appended to the end of the metric.
``AUTORECONNECT`` True           Automatically try to reconnect to graphite server.
================= ============== ============================================================

Only the most commons are given here. In fact, any parameters accepted by
`the graphitesend client`_ is also valid.

.. _`the graphitesend client`: https://github.com/daniellawrence/graphitesend
