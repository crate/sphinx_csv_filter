=================
Sphinx CSV Filter
=================

A Sphinx_ plugin that extends the csv-table_ reStructuredText_ directive to add
row filtering options.

Prerequisites
=============

You need to be using Sphinx and reStructuredText.

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

This plugin adds the ``:exclude:`` option to the csv-table_ directive. This option takes a Python dict specifying the column index (starting at zero) and a regular expression. Rows are excluded if the columnar value matches the supplied regular expression.

Here's an example::

    .. csv-table:: Example Table
       :header: Company,Contact,Country,Attend?
       :file: example.csv
       :exclude: {3: '(?i)Y\w*'}

In this example, rows from ``example.csv`` will be omitted from the output if the regular expression ``(?i)Y\w*`` matches value of the ``Attend?`` column.

Contributing
============

This project is primarily maintained by Crate.io_, but we welcome community
contributions!

See the `developer docs`_ and the `contribution docs`_ for more information.

Help
====

Looking for more help?

- Check `StackOverflow`_ for common problems
- Chat with us on `Slack`_
- Get `paid support`_

.. _contribution docs: CONTRIBUTING.rst
.. _Crate.io: http://crate.io/
.. _csv-table: http://docutils.sourceforge.net/docs/ref/rst/directives.html#csv-table
.. _developer docs: DEVELOP.rst
.. _paid support: https://crate.io/pricing/
.. _pip: https://pypi.python.org/pypi/pip
.. _reStructuredText: http://www.sphinx-doc.org/en/stable/rest.html
.. _Slack: https://crate.io/docs/support/slackin/
.. _Sphinx: http://www.sphinx-doc.org/en/stable/
.. _StackOverflow: https://stackoverflow.com/tags/crate
