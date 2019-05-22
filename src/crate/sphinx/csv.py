# -*- coding: utf-8; -*-

import ast
import re

from docutils.parsers.rst.directives.tables import CSVTable
from docutils.utils import SystemMessagePropagation

def include_dict(argument):
    return ast.literal_eval(argument)


def exclude_dict(argument):
    return ast.literal_eval(argument)


def non_negative_int(argument):
    """
    Converts the argument into an integer.
    Raises ValueError for negative or non-integer values.
    """
    value = int(argument)
    if value >= 0:
        return value
    else:
        raise ValueError('negative value defined; must be non-negative')


def non_negative_int_list(argument):
    """
    Converts a space- or comma-separated list of values into a Python list
    of integers.
    Raises ValueError for negative integer values.
    """
    if ',' in argument:
        entries = argument.split(',')
    else:
        entries = argument.split()
    return [non_negative_int(entry) for entry in entries]


class CSVFilterDirective(CSVTable):
    """ The CSV Filter directive renders csv defined in config
        and filter rows that contains a specified regex pattern
    """

    CSVTable.option_spec['include'] = include_dict
    CSVTable.option_spec['exclude'] = exclude_dict
    CSVTable.option_spec['included_cols'] = non_negative_int_list

    def parse_csv_data_into_rows(self, csv_data, dialect, source):
        rows, max_cols = super(CSVFilterDirective, self).parse_csv_data_into_rows(csv_data, dialect, source)
        if 'include' in self.options:
            rows = self._apply_include_filter(rows, max_cols, self.options['include'])
        if 'exclude' in self.options:
            rows = self._apply_exclude_filter(rows, max_cols, self.options['exclude'])
        if 'included_cols' in self.options:
            rows, max_cols = self._get_rows_with_included_cols(rows, self.options['included_cols'])
        return rows, max_cols

    def _apply_include_filter(self, rows, max_cols, include_dict):
        result = []

        # append row that contains filter at column index
        for row_idx, row in enumerate(rows):
            include = False
            if row_idx < self.options.get('header-rows', 0):
                # Always include header rows, if any
                include = True
            else:
                for col_idx, pattern in include_dict.items():
                    # cell data value is located at hardcoded index pos. 3
                    # data type is always a string literal
                    if max_cols - 1 >= col_idx:
                        print(pattern, row[col_idx][3][0], re.match(pattern, row[col_idx][3][0]))
                        if re.match(pattern, row[col_idx][3][0]):
                            include = True
                            break
            if include:
                result.append(row)

        return result

    def _apply_exclude_filter(self, rows, max_cols, exclude_dict):
        result = []

        # append row that does not contain filter at column index
        for row_idx, row in enumerate(rows):
            exclude = False
            if row_idx < self.options.get('header-rows', 0):
                # Always include header rows, if any
                exclude = False
            else:
                for col_idx, pattern in exclude_dict.items():
                    # cell data value is located at hardcoded index pos. 3
                    # data type is always a string literal
                    if max_cols - 1 >= col_idx:
                        if re.match(pattern, row[col_idx][3][0]):
                            exclude = True
                            break
            if not exclude:
                result.append(row)

        return result

    def _get_rows_with_included_cols(self, rows, included_cols_list):
        prepared_rows = []
        for row in rows:
            try:
                idx_row = [row[i] for i in included_cols_list]
                prepared_rows.append(idx_row)
            except IndexError:
                error = self.state_machine.reporter.error(
                    'One or more indexes of included_cols are not valid. '
                    'The CSV data does not contain that many columns.')
                raise SystemMessagePropagation(error)
        return prepared_rows, len(included_cols_list)


def setup(sphinx):
    sphinx.add_directive('csv-filter', CSVFilterDirective)
