import re
from copy import copy
from unittest import mock

import pytest
from crate.sphinx import csv
from crate.sphinx.csv import CSVFilterDirective


@pytest.mark.parametrize(
    "input, expected",
    [
        (1, 1),
        ("1", 1),
        (-1, ValueError()),
        ("-1", ValueError()),
        (object, TypeError())
    ]
)
def test_non_negative_int(input, expected):
    if isinstance(expected, Exception):
        with pytest.raises(expected.__class__):
            csv.non_negative_int(input)
    else:
        assert csv.non_negative_int(input) == expected


@pytest.mark.parametrize(
    "input, expected",
    [
        ("1,2,3,4", [1, 2, 3, 4]),
        ("a,2,3,4", ValueError()),
        ("-1,2,3,4", ValueError()),
        ("0,-2,3,4", ValueError()),
        (1, TypeError()),
    ]
)
def test_non_negative_int_list(input, expected):
    if isinstance(expected, Exception):
        with pytest.raises(expected.__class__):
            csv.non_negative_int_list(input)
    else:
        assert csv.non_negative_int_list(input) == expected


directive_params = ['Company,Contact,Country,Attend?'], None, 'source'

directive = CSVFilterDirective(
    None, None, None, None, None, None, None, None, None)
tmp_directive_options = {
    'header': 'Company,Contact,Country,Attend?',
    'delim': '\t',
    'file': 'example.csv',
    'included_cols': [0, 1, 2]
}


def test_csv_filter_exclude_directive():
    directive_options = copy(tmp_directive_options)
    directive_options['exclude'] = {3: r'(?i)Y\w*'}
    directive.options = directive_options

    with mock.patch.object(directive, '_apply_filters') as apply_filters:
        rows, max_cols = directive.parse_csv_data_into_rows(*directive_params)
        args = apply_filters.call_args
        assert args[0][2] is None
        assert args[0][3] == {3: re.compile(r'(?i)Y\w*', re.IGNORECASE)}


def test_csv_filter_include_directive():
    directive_options = copy(tmp_directive_options)
    directive_options['include'] = {3: r'(?i)Y\w*'}
    directive.options = directive_options

    with mock.patch.object(directive, '_apply_filters') as apply_filters:
        rows, max_cols = directive.parse_csv_data_into_rows(*directive_params)
        args = apply_filters.call_args
        assert args[0][2] == {3: re.compile(r'(?i)Y\w*', re.IGNORECASE)}
        assert args[0][3] is None


def test_csv_filter_include_exclude_directive():
    directive_options = copy(tmp_directive_options)
    directive_options['include'] = {3: r'(?i)Y\w*'}
    directive_options['exclude'] = {3: r'(?i)N\w*'}
    directive.options = directive_options

    with mock.patch.object(directive, '_apply_filters') as apply_filters:
        rows, max_cols = directive.parse_csv_data_into_rows(*directive_params)
        args = apply_filters.call_args
        assert args[0][2] == {3: re.compile(r'(?i)Y\w*', re.IGNORECASE)}
        assert args[0][3] == {3: re.compile(r'(?i)N\w*', re.IGNORECASE)}


rows = [
    [
        (0, 0, 0, ['Centro comercial Moctezuma']),
        (0, 0, 0, ['Francisco Chang']),
        (0, 0, 0, ['Mexico']),
        (0, 0, 0, ['YES']),
    ],
    [
        (0, 0, 0, ['Alfreds Futterkiste']),
        (0, 0, 0, ['Maria Anders']),
        (0, 0, 0, ['Germany']),
        (0, 0, 0, ['y']),
    ],
    [
        (0, 0, 0, ['Ernst Handel']),
        (0, 0, 0, ['Roland Mendel']),
        (0, 0, 0, ['Austria']),
        (0, 0, 0, ['NO']),
    ],
    [
        (0, 0, 0, ['Wernher von Braun']),
        (0, 0, 0, ['Hans Koenigsmann']),
        (0, 0, 0, ['‎Germany']),
        (0, 0, 0, []),  # Empty cell
    ]
]


def test_apply_none_filters():
    result = directive._apply_filters(rows, 4, None, None)
    assert result == rows


def test_apply_exclude_filters():
    exclude_filters = {3: re.compile(r'(?i)Y\w*', re.IGNORECASE)}
    result = directive._apply_filters(rows, 4, None, exclude_filters)
    assert result == [rows[2], rows[3]]


def test_apply_multi_exclude_filters():
    exclude_filters = {
        0: re.compile(r'Centro', re.IGNORECASE),
        3: re.compile(r'NO', re.IGNORECASE)
    }
    result = directive._apply_filters(rows, 4, None, exclude_filters)
    assert result == [rows[1], rows[3]]


def test_apply_include_filters():
    include_filter = {3: re.compile(r'(?i)n\w*', re.IGNORECASE)}
    result = directive._apply_filters(rows, 4, include_filter, None)
    assert result == [rows[2]]


def test_apply_multi_include_filters():
    include_filter = {
        2: re.compile(r'Ger', re.IGNORECASE),
        3: re.compile(r'y', re.IGNORECASE)
    }
    result = directive._apply_filters(rows, 4, include_filter, None)
    assert result == [rows[1]]


def test_apply_include_exclude_filters():
    include_filter = {0: re.compile(r'^[CE].+$', re.IGNORECASE)}
    exclude_filter = {1: re.compile(r'^Rolan.+$', re.IGNORECASE)}
    result = directive._apply_filters(rows, 4, include_filter, exclude_filter)
    assert result == [rows[0]]
