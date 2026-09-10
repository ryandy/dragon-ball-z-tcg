import abc
import time

from dbz.state import State


class IOBackend(abc.ABC):
    @abc.abstractmethod
    def write(self, line):
        '''Receives one already-wrapped line of game text.'''

    @abc.abstractmethod
    def read_choice(self, prompt):
        '''Blocks and returns raw text the way input() does today.'''


class CLIBackend(IOBackend):
    '''Preserves current terminal behavior, including the typewriter
    pacing that used to live in util.py's _wait().'''

    def __init__(self):
        self._last_write_time = None

    def write(self, line):
        self._pace()
        print(line)

    def read_choice(self, prompt):
        return input(prompt)

    def _pace(self):
        if State.INTERACTIVE and self._last_write_time is not None:
            print_period = 1.0 / State.PRINT_FREQUENCY
            time_elapsed = time.time() - self._last_write_time
            time.sleep(max(0, print_period - time_elapsed))
        self._last_write_time = time.time()


# Default backend preserves current terminal behavior. Swap by assigning
# State.IO_BACKEND (e.g. to a browser bridge backend in a future step).
if State.IO_BACKEND is None:
    State.IO_BACKEND = CLIBackend()
