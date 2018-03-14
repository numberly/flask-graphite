Carbon aggregator
#################

Why is it needed ?
==================

A running carbon-aggregator instance is needed to use Flask-Graphite.

Since a data point is sent for each requests, they must be aggregated to be
useful. Even if they was buffered, any application with multiple workers would
still need to aggregate the time series.

If they weren't, each data point would override the previous one, and only the
last point received each minute would be considered.

Configuring carbon-aggregator
=============================

You can setup the aggregation rules based on the end of metric names, if you're
sure it will not collide with other applications.

As a general rule, counter metrics should be summed, while others should be
averaged. Below is a list of aggregation suitable for a simple environment.

.. code-block:: none

    <route>.count (60) = sum <<route>>.count
    <route>.status_code.<type> (60) = sum <<route>>.status_code.<type>
    <route>.pt (60) = avg <<route>>.pt
    <route>.size (60) = avg <<route>>.size

