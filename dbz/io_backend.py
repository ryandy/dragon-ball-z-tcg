import abc
import json
import time

from dbz.state import State


class IOBackend(abc.ABC):
    @abc.abstractmethod
    def write(self, line):
        '''Receives one already-wrapped line of game text.'''

    @abc.abstractmethod
    def read_choice(self, prompt, names=None, descriptions=None,
                     other_names=None, other_descriptions=None, allow_pass=True,
                     targets=None, other_targets=None):
        '''Blocks and returns raw text the way input() does today.

        prompt is the short, plain-text label for this choice (e.g.
        "Select a Non-Combat card to play from your hand") - it's up to
        each backend to dress it up for its own medium (CLIBackend wraps
        it as an input() prompt; BrowserBackend shows it as-is above the
        choice cards). The fully-formatted, numbered listing is a
        separate, already-sent write() line - see Player.choose().

        names/descriptions/other_names/other_descriptions/allow_pass are
        Player.choose()'s own parameters, forwarded through unchanged, for
        backends that want the structured option data (e.g. to render
        clickable cards) instead of/in addition to the pre-formatted
        prompt text already sent via write().

        targets/other_targets are parallel to names/other_names: the uid of
        the board card each option refers to (see util.ui_target), or None,
        so a UI can let the player click the card on the board.'''

    def write_state(self, snapshot):
        '''Receives a JSON-serializable board-state snapshot (see
        Runner.build_state_snapshot). No-op by default - CLIBackend has
        no use for it since the terminal already shows state via write().'''
        pass

    def announce(self, event, ack=False):
        '''Receives a JSON-serializable game event (see util.announce_play).
        If ack is True, blocks until the player acknowledges it. No-op by
        default - CLIBackend has no use for it since the terminal already
        shows the same information as text via write().'''
        pass


class CLIBackend(IOBackend):
    '''Preserves current terminal behavior, including the typewriter
    pacing that used to live in util.py's _wait().'''

    def __init__(self):
        self._last_write_time = None

    def write(self, line):
        self._pace()
        print(line)

    def read_choice(self, prompt, **kwargs):
        return input(f'>>> {prompt}: ')

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

    def read_choice(self, prompt, names=None, descriptions=None,
                     other_names=None, other_descriptions=None, allow_pass=True,
                     targets=None, other_targets=None):
        from js import dbzReadChoice
        if State.RUNNER is not None:
            State.RUNNER.refresh_state()
        options = json.dumps({
            'kind': 'choice',
            'prompt': prompt,
            'names': names or [],
            'descriptions': descriptions or [],
            'otherNames': other_names or [],
            'otherDescriptions': other_descriptions or [],
            'allowPass': bool(allow_pass),
            'targets': targets or [None] * len(names or []),
            'otherTargets': other_targets or [None] * len(other_names or []),
        })
        return dbzReadChoice(options)

    def write_state(self, snapshot):
        from js import postMessage
        postMessage(json.dumps({'type': 'state', 'snapshot': snapshot}))

    def announce(self, event, ack=False):
        from js import dbzReadChoice, postMessage
        postMessage(json.dumps({'type': 'event', 'event': event, 'ack': ack}))
        if ack:
            if State.RUNNER is not None:
                State.RUNNER.refresh_state()
            dbzReadChoice(json.dumps({'kind': 'ack'}))


# Default backend preserves current terminal behavior. Swap by assigning
# State.IO_BACKEND (e.g. to BrowserBackend() inside a Pyodide worker).
if State.IO_BACKEND is None:
    State.IO_BACKEND = CLIBackend()
