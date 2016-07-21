# -*- coding: utf-8; -*-

import csv
import ast
import re

from docutils.parsers.rst.directives.tables import CSVTable
from docutils.utils import SystemMessagePropagation
from docutils import statemachine
from docutils.parsers.rst import directives

class CSVFilterDirective(CSVTable):
    """ The CSV Filter directive renders csv defined in config
        and filter rows that contains a specified string
    """

    CSVTable.option_spec['exclude'] = directives.unchanged

    def parse_csv_data_into_rows(self, csv_data, dialect, source):
        rows, max_cols = super().parse_csv_data_into_rows(csv_data, dialect, source)
        if 'exclude' in self.options:
            exclude_dict = ast.literal_eval(self.options['exclude'])
            rows = self._apply_filter(rows, exclude_dict)
        return rows, max_cols

    def _apply_filter(self, rows, exclude_dict):
        result = []

        # append row that does not contain filter at column index
        for row in rows:
            exclude = False
            for col_idx, pattern in exclude_dict.items():
                # cell data value is located at hardcoded index pos. 3
                # data type is always a string literal
                try:
                    val = row[col_idx][3][0]
                    if re.match(pattern, val):
                        exclude = True
                        break
                except IndexError:
                    error = self.state_machine.reporter.error(
                        'Insufficient data supplied. Number of defined headers do not match ' 
                        'the number of columns in the table data')
                    raise SystemMessagePropagation(error)
                
            if not exclude:
                result.append(row)

        return result

def setup(sphinx):
    sphinx.add_directive('csv-table', CSVFilterDirective)
