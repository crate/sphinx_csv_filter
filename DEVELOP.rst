===============
Developer Guide
===============

Setup
=====

This project uses buildout_ to set up the development environment.

To start things off, run::

    $ python -m venv .venv
    $ source .venv/bin/activate

Then, run::

    $ pip install -e .

Test
====

To get the test dependencies run the following command::

    $ pip install -e .[testing]

To run the tests::

    $ pytest

The plugin can be tested by running::

    $ python setup.py build_sphinx

The output of a rendered example CSV can be found in the ``out/html`` directory.

Preparing a Release
===================

To create a new release, you must:

- Update ``version`` in ``setup.py``

- Add a section for the new version in the ``CHANGES.txt`` file

- Commit your changes with a message like "prepare release x.y.z"

- Push to ``origin/master``

- Create a tag by running ``./devtools/create_tag.sh``

PyPI Deployment
===============

To install the development dependencies run the following command::

    $ pip install -e .[development]

To create the package use::

    $ python setup.py sdist bdist_wheel

Then, use twine_ to upload the package to PyPI_::

    $ python -m twine upload dist/*

For this to work, you will need a personal PyPI account that is set up as a project admin.

You'll also need to create a ``~/.pypirc`` file, like so::

    [distutils]
    index-servers =
      pypi

    [pypi]
    repository=https://pypi.python.org/pypi
    username=<USERNAME>
    password=<PASSWORD>

Here, ``<USERNAME>`` and ``<PASSWORD>`` should be replaced with your username and password, respectively.

If you want to check the PyPI description before uploading, run::

    $ python -m twine check dist/*

.. _buildout: https://pypi.python.org/pypi/zc.buildout
.. _PyPI: https://pypi.python.org/pypi
.. _twine: https://pypi.python.org/pypi/twine
