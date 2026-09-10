import abc
import json
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


class BrowserBackend(IOBackend):
    '''Runs inside a Pyodide Web Worker (see web/worker.js). Posts output
    lines to the main thread as JSON instead of printing.

    read_choice() blocks this worker thread (not the main/UI thread) via
    a synchronous Atomics.wait bridge implemented in JS (worker.js's
    dbzReadChoice), following Pyodide's documented pattern for
    synchronous I/O from a worker. A headless CPU-vs-CPU game never
    calls it: Player.choose() (dbz/player.py) short-circuits through the
    AI path and returns before reaching IO_BACKEND.read_choice() whenever
    a player is non-interactive.'''

    def write(self, line):
        from js import postMessage  # only importable inside a JS runtime
        postMessage(json.dumps({'type': 'write', 'line': line}))

    def read_choice(self, prompt):
        from js import dbzReadChoice
        return dbzReadChoice(prompt)


# Default backend preserves current terminal behavior. Swap by assigning
# State.IO_BACKEND (e.g. to BrowserBackend() inside a Pyodide worker).
if State.IO_BACKEND is None:
    State.IO_BACKEND = CLIBackend()
