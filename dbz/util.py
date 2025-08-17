import itertools
import sys
import time

import tabulate

from dbz.state import State


_dprint_time = None
def dprint(msg='', quiet=None):
    if quiet is False or State.QUIET is False:
        for line in msg.split('\n'):
            splitlines = _split_msg_by_width_and_indent(line)
            for splitline in splitlines:
                _wait()
                print(splitline)


def dprint_table(table, quiet=None):
    tabulate.PRESERVE_WHITESPACE = True
    column_count = len(table)
    assert column_count >= 1

    column_width = (State.PRINT_WIDTH - (column_count + 1)) / column_count - 2
    new_table = []
    for column in range(column_count):
        # Check if columns need to be different widths
        # Note: this only works for up to 2 columns
        # Note: column0 ends up on the right - visually we want it to be the wider column
        if column == 0 and column_width % 1:
            column_width += 1
        elif column == 1 and column_width % 1:
            column_width -= 1
        new_column = []
        for cell in table[column]:
            new_cell = []
            for line in cell.split('\n'):
                splitlines = _split_msg_by_width_and_indent(line, width=int(column_width))
                #print('~~', column_width, column, splitlines)
                new_cell.extend(splitlines)
            new_column.append('\n'.join(new_cell))
        new_table.append(new_column)

    table = itertools.zip_longest(*reversed(new_table))
    table = tabulate.tabulate(table, tablefmt='fancy_grid')
    dprint(table, quiet=quiet)


def _wait():
    global _dprint_time
    # Track time of last dprint and sleep until target period before the next print
    if State.INTERACTIVE and _dprint_time is not None:
        print_period = 1.0 / State.PRINT_FREQUENCY
        time_elapsed = time.time() - _dprint_time
        time.sleep(max(0, print_period - time_elapsed))
    _dprint_time = time.time()


def _split_msg_by_width_and_indent(msg, width=None):
    width = State.PRINT_WIDTH if width is None else width

    lines = []
    count = 0
    indent = _get_indent(msg)
    while len(msg):
        if count > 0:
            msg = f'{" " * indent}{msg}'
        cur_width = State.PRINT_WIDTH if width is None else width
        if cur_width < len(msg):
            while msg[cur_width] != ' ':
                #print('-->', cur_width, msg, len(msg))
                cur_width -= 1
        chunk = msg[:cur_width].ljust(width)
        if cur_width < len(msg) and msg[cur_width] == ' ':
            cur_width += 1
        msg = msg[cur_width:]
        lines.append(chunk)
        #print(f'chunk: "{chunk}" len={len(chunk)}')
        count += 1
    return lines or ['']


def _get_indent(s):
    idx = 0
    while idx < len(s) and (s[idx] == ' ' or s[idx] == '-'):
        idx += 1
    return idx
