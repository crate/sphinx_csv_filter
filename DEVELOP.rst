=============================
Sphinx CSV Filter Development
=============================

Development Setup
=================

To get a development environment crate-python uses `buildout
<https://pypi.python.org/pypi/zc.buildout/2.5.2>`_

Run `bootstrap.py`::

    python bootstrap.py

And afterwards run buildout::

    ./bin/buildout -N

Test
====

The plugin can be tested by running::

    bin/sphinx

in the terminal. The output of a rendered example CSV can be found in the
``out/html`` directory.

Deployment to Pypi
==================

To create the packages use::

    bin/py setup.py sdist bdist_wheel

and then use `twine <https://pypi.python.org/pypi/twine>`_ to upload the
packages::

    twine upload dist/*

If twine is not installed locally the regular setup.py upload can also be used,
but does only support plaintext authentication::

    bin/py setup.py sdist upload