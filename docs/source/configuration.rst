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

Here is a succinct list of different options available, and their respective
meanings.

================================== ============== =============================================================================================================
NAME                               Default        Description
================================== ============== =============================================================================================================
``FLASK_GRAPHITE_HOST``            localhost      The host of the carbon-aggregator installation.
``FLASK_GRAPHITE_PORT``            2023           The port of the carbon-aggregator installation.
``FLASK_GRAPHITE_PREFIX``                         A prefix that will be prepended to all metrics.
``FLASK_GRAPHITE_GROUP``           flask-graphite A string that will be added between the host and the actual metric name to generate the complete metric name.
``FLASK_GRAPHITE_AUTORECONNECT``   True           Automatically try to reconnect to graphite server.
``FLASK_GRAPHITE_METRIC_TEMPLATE`` url_rule       The Flask ``request``'s attribute that should be used to generate the metric name.
================================== ============== =============================================================================================================

.. hint::
   Any parameter accepted by `the graphitesender client`_ is also valid when
   prefixed with ``FLASK_GRAPHITE_``.

.. _`the graphitesender client`: https://github.com/Shir0kamii/graphitesender
