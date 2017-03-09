================
Gathered metrics
================

After each request, some metrics are sent to carbon. Each metrics uses the
``after_request`` hooks to be compute and send the good value.

A different metric is used for each route of the application.

Metric format
-------------

The `URL Rule`_ matched by the requested is parsed to create the `route`
part of the metric.

The parsing happens on the URI of the `URL Rule`_. Each converter_ within
this URI is replaced with its variable name and the slash characters are
replaced with dot characters. Below are some examples of such transformations:

===============================  ========================
matched URI                      corresponding route part
===============================  ========================
/foo                             foo
/foo/bar/baz                     foo.bar.baz
/foo/<int:bar>                   foo.bar
/foo/<string:bar>/baz/<int:boo>  foo.bar.baz.boo
===============================  ========================

In addition to this route part, a suffix is used depending on the metric sent.
These parts are covered in the next section.

List of the gathered metrics
----------------------------

In this section, ``<route>`` refer to the route part as described in the
previous section. the ``<status_code>`` placeholed represents the status code
sent in response, to the request, and the ``<status_type>`` is simply the
first digit of the status code.

=================  ===================================  ================================================
name               metrics                              value
=================  ===================================  ================================================
processing time    <route>.pt                           The processing time of the route
number of request  <route>.count                        The number of request received on this route
size of request    <route>.size                         The size of the response for this route
status code        <route>.status_code.<status_code>    A counter for each status_code received
status type        <route>.status_type.<status_type>XX  A counter for each type of status code (eg. 2XX)
=================  ===================================  ================================================


.. _`URL Rule`: http://werkzeug.pocoo.org/docs/latest/routing/
.. _converter: http://werkzeug.pocoo.org/docs/0.11/routing/#builtin-converters
