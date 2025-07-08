import sys
import time

from dbz.state import State


_dprint_time = None
def dprint(msg='', quiet=None):
    if quiet is False or State.QUIET is False:
        for line in msg.split('\n'):
            _print_with_width_and_indent(line)


def _wait():
    global _dprint_time
    # Track time of last dprint and sleep until target period before the next print
    if State.INTERACTIVE and _dprint_time is not None:
        print_period = 1.0 / State.PRINT_FREQUENCY
        time_elapsed = time.time() - _dprint_time
        time.sleep(max(0, print_period - time_elapsed))
    _dprint_time = time.time()


def _print_with_width_and_indent(msg):
    if not msg:
        _wait()
        print()
        return

    count = 0
    indent = _get_indent(msg)
    while len(msg):
        if count > 0:
            msg = f'{" " * indent}{msg}'
        width = State.PRINT_WIDTH
        if width < len(msg):
            while msg[width] != ' ':
                width -= 1
            width += 1
        chunk = msg[:width]
        msg = msg[width:]
        _wait()
        print(chunk)
        count += 1


def _get_indent(s):
    idx = 0
    while idx < len(s) and (s[idx] == ' ' or s[idx] == '-'):
        idx += 1
    return idx
