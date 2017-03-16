==========================
Configuring Flask-Graphite
==========================

How to configure Flask-Graphite?
--------------------------------

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

Configuring carbon-aggregator
-----------------------------

A running carbon-aggregator instance is needed to use Flask-Graphite. This is
because if there are multiple workers on the same hosts, their metrics will end
on the same name.

You can setup the aggregation rules based on the end of metric names, if you're
sure it will not collide with other applications.

As a general rule, counter metrics should be summed, while others should be
averaged. Below is a list of aggregation suitable for a simple environment.

.. code-block:: none

    <route>.count (60) = sum <<route>>.count
    <route>.status_code.<type> (60) = sum <<route>>.status_code.<type>
    <route>.pt (60) = avg <<route>>.pt
    <route>.size (60) = avg <<route>>.size

