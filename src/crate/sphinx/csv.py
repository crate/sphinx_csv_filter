# -*- coding: utf-8; -*-

import ast
import re

from docutils.parsers.rst.directives.tables import CSVTable
from docutils.utils import SystemMessagePropagation


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
    CSVTable.option_spec['include'] = ast.literal_eval
    CSVTable.option_spec['exclude'] = ast.literal_eval
    CSVTable.option_spec['included_cols'] = non_negative_int_list

    def parse_csv_data_into_rows(self, csv_data, dialect, source):
        rows, max_cols = super(
            CSVFilterDirective, self
        ).parse_csv_data_into_rows(csv_data, dialect, source)
        include_filters = exclude_filters = None
        if 'include' in self.options:
            include_filters = {
                k: re.compile(v) for k, v in self.options['include'].items()
            }
        if 'exclude' in self.options:
            exclude_filters = {
                k: re.compile(v) for k, v in self.options['exclude'].items()
            }
        rows = self._apply_filters(rows, max_cols, include_filters, exclude_filters)
        if 'included_cols' in self.options:
            rows, max_cols = self._get_rows_with_included_cols(
                rows, self.options['included_cols']
            )
        return rows, max_cols

    def _apply_filters(self, rows, max_cols, include_filters, exclude_filters):
        result = []

        header_rows = self.options.get('header-rows', 0)
        # Always include header rows, if any
        result.extend(rows[:header_rows])

        for row in rows[header_rows:]:
            # We generally include a row, ...
            include = True
            if include_filters:
                for col_idx, pattern in include_filters.items():
                    # cell data value is located at hardcoded index pos. 3
                    # data type is always a string literal
                    if max_cols - 1 >= col_idx:
                        # sanitize to empty string if cell is empty
                        cell = row[col_idx][3][0] if row[col_idx][3] else ""
                        if not pattern.match(cell):
                            # ... unless any of the include filters do not match
                            # its cell ...
                            include = False
                            break

            # ... or unless exclude filters are defined (as well) ...
            if include and exclude_filters:
                for col_idx, pattern in exclude_filters.items():
                    # cell data value is located at hardcoded index pos. 3
                    # data type is always a string literal
                    if max_cols - 1 >= col_idx:
                        # sanitize to empty string if cell is empty
                        cell = row[col_idx][3][0] if row[col_idx][3] else ""
                        if pattern.match(cell):
                            # ... then we exclude a row if any of the defined
                            # exclude filters matches its cell.
                            include = False
                            break

            if include:
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
