import sys
import time

from state import State


def dprint(msg=''):
    if State.INTERACTIVE:
        time.sleep(0.1)
    print(msg)
