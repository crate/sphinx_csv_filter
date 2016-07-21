Spinx CSV Filter
=====================

This is a sphinx plugin that extends ``csv-table`` directive of the
``docutils`` text-processing system. It appends additional filter options 
which exclude rows of a given CSV table.

Features
--------

-  [x] Filters rows of a referenced CSV table that contains a regex pattern 
   at a given column index.

Installation
------------

To include the extension add the following line to the ``config.py`` in
your Sphinx-Project.

::

    extensions = ['crate.sphinx.csv']

If you have other extensions use:

::

    extensions.append('crate.sphinx.csv')

First Example
-------------

This example excludes all rows if the value of column ``Attend?`` (Idx: 3)
matches the regex pattern.

::

    .. csv-table:: Example Table
       :header: Company,Contact,Country,Attend?
       :file: example.csv
       :exclude: {3: '(?i)Y\w*'}

Options
~~~~~~~

-  ``:exclude:``: Python dictionary that defines on which **column indizes** 
   the **regex pattern** are applied.