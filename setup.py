# -*- coding: utf-8; -*-
#
# Licensed to Crate.IO GmbH ("Crate") under one or more contributor
# license agreements.  See the NOTICE file distributed with this work for
# additional information regarding copyright ownership.  Crate licenses
# this file to you under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.  You may
# obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  See the
# License for the specific language governing permissions and limitations
# under the License.
#
# However, if you have executed another commercial license agreement
# with Crate these terms will supersede the license and you may use the
# software solely pursuant to the terms of the relevant commercial agreement.

import os

from setuptools import find_packages, setup


def read(path):
    with open(os.path.join(os.path.dirname(__file__), path)) as f:
        return f.read()


setup(
    name='sphinx-csv-filter',
    version='0.4.2',
    url='https://github.com/crate/sphinx_csv_filter',
    author='Crate.IO GmbH',
    author_email='office@crate.io',
    package_dir={'': 'src'},
    description='A CSV filter directive for docutils and Sphinx, that extends the '
                '"csv-table" reStructuredText directive to add row filtering options.',
    long_description=read('README.rst'),
    long_description_content_type='text/x-rst',
    platforms=['any'],
    license='Apache License 2.0',
    keywords='sphinx csv filter docutils directive plugin '
             'csv-table csv-filter restructuredtext',
    packages=find_packages('src'),
    namespace_packages=['crate'],
    entry_points={},
    extras_require={
        "development": [
            "build",
            "setuptools",
            "twine",
            "wheel",
        ],
        "testing": [
            "flake8",
            "pytest",
            "pytest-cov",
            "pytest-flake8",
            "pytest-isort",
        ]
    },
    install_requires=[
        "Sphinx",
    ],
    python_requires=">=3.3",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Documentation',
        'Topic :: Documentation :: Sphinx',
        'Topic :: Education',
        'Topic :: Software Development :: Code Generators',
        'Topic :: Software Development :: Documentation',
        'Topic :: Text Processing :: Markup :: reStructuredText',
    ],
)
