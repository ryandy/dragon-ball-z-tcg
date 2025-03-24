import sys
import time

from state import State


_dprint_time = None
def dprint(msg=''):
    global _dprint_time

    # Track time of last dprint and sleep until target period before the next print
    if State.INTERACTIVE and _dprint_time is not None:
        print_period = 1.0 / State.PRINT_FREQUENCY
        time_elapsed = time.time() - _dprint_time
        time.sleep(max(0, print_period - time_elapsed))

    _dprint_time = time.time()
    print(msg)
