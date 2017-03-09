==========================
Configuring Flask-Graphite
==========================

How to configure Flask-Graphite ?
---------------------------------

You can configure Flask-Graphite through the application's configuration.

The ``FLASK_GRAPHITE_`` namespace will be fetched for the application's
configuration and used as Flask-Graphite own configuration.

Configuration keys
------------------

Here is a succint list of the different options available, and their respective
meanings. The prefix ``FLASK_GRAPHITE_`` is removed for readability.

=============== ============================================================
``HOST``        The host of the carbon-aggregator installation.
``PORT``        The port of the carbon-aggregator installation.
``PREFIX``      A prefix that will be prepended to all metrics.
``GROUP``       A string that will be added between the host and the actual.
                metric name to generate the complete metric name.
``DEBUG``       Enable debug flag on graphitesend.
``SYSTEM_NAME`` The name of the system which sends the metrics (hostname)
``SUFFIX``      A suffix appended to the end of the metric.
=============== ============================================================

Only the most commons are given here. In fact, any parameters accepted by
`the graphitesend client`_ is also valid.

We strongly encourage you to set the ``GROUP`` option to separate the
flask-graphite metrics from others.


.. _`the graphitesend client`: https://github.com/daniellawrence/graphitesend
