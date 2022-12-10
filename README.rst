=================
Sphinx CSV filter
=================

.. image:: https://github.com/crate/sphinx_csv_filter/workflows/tests.yml/badge.svg
    :target: https://github.com/crate/sphinx_csv_filter/actions/workflows/tests.yml
    :alt: CI outcome

.. image:: https://codecov.io/gh/crate/sphinx_csv_filter/branch/master/graph/badge.svg
    :target: https://app.codecov.io/gh/crate/sphinx_csv_filter
    :alt: Test suite code coverage

.. image:: https://img.shields.io/pypi/v/sphinx-csv-filter.svg
    :target: https://pypi.org/project/sphinx-csv-filter/
    :alt: Supported Python versions

.. image:: https://img.shields.io/pypi/pyversions/sphinx-csv-filter.svg
    :target: https://pepy.tech/project/sphinx-csv-filter
    :alt: Package version on PyPI

.. image:: https://pepy.tech/badge/sphinx-csv-filter/month
    :target: https://pepy.tech/project/sphinx-csv-filter
    :alt: PyPI downloads per month

.. image:: https://img.shields.io/pypi/status/sphinx-csv-filter.svg
    :target: https://pypi.org/project/sphinx-csv-filter/
    :alt: Project status (alpha, beta, stable)

.. image:: https://img.shields.io/pypi/l/sphinx-csv-filter.svg
    :target: https://pypi.org/project/sphinx-csv-filter/
    :alt: License

|

A CSV filter directive for docutils and `Sphinx`_, that extends the
"`csv-table`_" `reStructuredText`_ directive to add row filtering options.

Details
=======

The package depends on ``docutils``, it provides a ``CSVFilterDirective``,
extending ``CSVTable``. When used as a Sphinx extension, it will register the
``csv-filter`` `Sphinx directive`_.

Installation
============

The Sphinx CSV filter plugin is available as a pip_ package.

To install, run::

    $ pip install sphinx-csv-filter

To update, run::

    $ pip install -U sphinx-csv-filter

Set Up
======

To include the extension, add this line to ``config.py`` in
your Sphinx project::

    extensions = ['crate.sphinx.csv']

If you're using other extensions, edit the existing list, or add this::

    extensions.append('crate.sphinx.csv')

Use
===

This plugin adds the following options to the csv-table_ directive:

``:included_cols:``
    This is a comma-separated list of column indexes to include in the output.

``:include:``
    This option takes a Python dict specifying the column index (starting at
    zero) and a regular expression. Rows are included if the columnar value
    matches the supplied regular expression.

``:exclude:``
    This option takes a Python dict specifying the column index (starting at
    zero) and a regular expression. Rows are excluded if the columnar value
    matches the supplied regular expression.

If a row matches an ``:include:`` as well as an ``:exclude:`` filter, the row
with be excluded.

Here's an example::

    .. csv-filter:: Example Table
       :header: Company,Contact,Country,Attend?
       :file: example.csv
       :exclude: {3: '(?i)Y\w*'}

In this example, rows from ``example.csv`` will be omitted from the output if the regular expression ``(?i)Y\w*`` matches value of the ``Attend?`` column.

Contributing
============

This project is primarily maintained by `Crate.IO`_, but we welcome community
contributions!

See the `developer docs`_ and the `contribution docs`_ for more information.

Help
====

Looking for more help?

- Check out our `support channels`_.

.. _contribution docs: CONTRIBUTING.rst
.. _Crate.IO: https://crate.io/
.. _csv-table: https://docutils.sourceforge.io/docs/ref/rst/directives.html#csv-table
.. _developer docs: DEVELOP.rst
.. _pip: https://pypi.org/project/pip/
.. _reStructuredText: https://www.sphinx-doc.org/en/stable/rest.html
.. _Sphinx: https://www.sphinx-doc.org/
.. _Sphinx directive: https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html
.. _support channels: https://crate.io/support/
