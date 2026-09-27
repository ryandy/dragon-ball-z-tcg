// Pyodide v314.x ships as an ES module (pyodide.asm.mjs); classic workers
// with importScripts() are no longer supported, so this must be loaded as
// a module worker (see web/main.js's `new Worker(..., {type: 'module'})`).
import { loadPyodide } from 'https://cdn.jsdelivr.net/pyodide/v314.0.6/full/pyodide.mjs';

const DBZ_WHEEL = './dist/dbz_tcg-0.0.1-py3-none-any.whl';

// Shared-memory layout for the synchronous input bridge (P1b). controlArray
// is an Int32Array over a SharedArrayBuffer supplied by main.js:
//   [0] = wait flag (Atomics.wait target - reset to 0 before each request)
//   [1] = byte length of the UTF-8 answer written into textView
const CONTROL_FLAG = 0;
const CONTROL_LENGTH = 1;
let controlArray = null;
let textView = null;

let pyodideReadyPromise = init();

async function init() {
  const pyodide = await loadPyodide();
  await pyodide.loadPackage(['numpy', 'micropip']);

  const micropip = pyodide.pyimport('micropip');
  await micropip.install('tabulate');
  await micropip.install(new URL(DBZ_WHEEL, self.location.href).href);

  let decks;
  try {
    decks = await listDecks(pyodide);
  } catch (err) {
    postMessage(JSON.stringify({type: 'error', message: `listDecks failed: ${err}`}));
    throw err;
  }
  postMessage(JSON.stringify({type: 'ready', decks}));
  return pyodide;
}

// Lists dbz/decks/* (excluding editor backup files like 'goku_survive~')
// so the UI's deck selects always match whatever decks are actually
// bundled in the wheel, instead of a hardcoded JS list.
async function listDecks(pyodide) {
  await pyodide.runPythonAsync(`
    import pathlib
    import dbz

    _decks_dir = pathlib.Path(dbz.__file__).parent / 'decks'
    _deck_names = sorted(
        p.name for p in _decks_dir.iterdir()
        if p.is_file() and not p.name.endswith('~'))
  `);
  return pyodide.globals.get('_deck_names').toJs();
}

// Called synchronously from Python (dbz.io_backend.BrowserBackend.read_choice)
// via Pyodide's js interop. optionsJson is a JSON string with
// {prompt, names, descriptions, otherNames, otherDescriptions, allowPass}
// (see BrowserBackend.read_choice). Blocks this worker thread only - the
// main/UI thread stays responsive and is what actually collects the
// human's answer - using Pyodide's documented Atomics.wait pattern for
// synchronous I/O from a worker.
self.dbzReadChoice = function (optionsJson) {
  const options = JSON.parse(optionsJson);
  postMessage(JSON.stringify({type: 'need_input', ...options}));
  Atomics.store(controlArray, CONTROL_FLAG, 0);
  Atomics.wait(controlArray, CONTROL_FLAG, 0);
  const length = Atomics.load(controlArray, CONTROL_LENGTH);
  return new TextDecoder().decode(textView.slice(0, length));
};

// SEED/DECK1_NAME/DECK2_NAME are passed in as Pyodide globals (set by
// runGame's caller) rather than interpolated into this source string, so
// user-controlled values never get spliced into Python source text.
const INTERACTIVE_CODE = `
  import random

  from dbz.deck import Deck
  from dbz.io_backend import BrowserBackend
  from dbz.runner import Runner
  from dbz.state import State

  random.seed(SEED)
  State.SEED = SEED
  State.IO_BACKEND = BrowserBackend()
  State.INTERACTIVE = True
  State.QUIET = False

  deck1 = Deck.from_spec(DECK1_NAME)
  deck2 = Deck.from_spec(DECK2_NAME)
  runner = Runner(deck1, deck2)
  winning_player_num = runner.run()
`;

async function runInteractive(seed, deck1, deck2) {
  const pyodide = await pyodideReadyPromise;
  try {
    pyodide.globals.set('SEED', seed);
    pyodide.globals.set('DECK1_NAME', deck1);
    pyodide.globals.set('DECK2_NAME', deck2);
    await pyodide.runPythonAsync(INTERACTIVE_CODE);
    const winner = pyodide.globals.get('winning_player_num');
    postMessage(JSON.stringify({type: 'done', winner}));
  } catch (err) {
    postMessage(JSON.stringify({type: 'error', message: String(err)}));
  }
}

self.onmessage = async (event) => {
  const {type} = event.data;

  if (type === 'init_sab') {
    controlArray = new Int32Array(event.data.controlSAB);
    textView = new Uint8Array(event.data.textSAB);
  } else if (type === 'run_interactive') {
    const {seed, deck1, deck2} = event.data;
    await runInteractive(seed, deck1, deck2);
  }
};
