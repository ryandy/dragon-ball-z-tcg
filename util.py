import sys
import time

from state import State


def dprint(msg=''):
    if State.ENABLE_INTERACTIVE:
        time.sleep(0.1)
    print(msg)
