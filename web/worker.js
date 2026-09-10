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

  postMessage(JSON.stringify({type: 'ready'}));
  return pyodide;
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

function cpuVsCpuCode(seed) {
  return `
    import random

    from dbz.deck import Deck
    from dbz.io_backend import BrowserBackend
    from dbz.runner import Runner
    from dbz.state import State

    random.seed(${seed})
    State.IO_BACKEND = BrowserBackend()
    State.INTERACTIVE = False
    State.QUIET = False

    deck1 = Deck.from_spec('goku_survival')
    deck2 = Deck.from_spec('goku_survival')
    runner = Runner(deck1, deck2)
    winning_player_num = runner.run()
  `;
}

function interactiveCode(seed) {
  return `
    import random

    from dbz.deck import Deck
    from dbz.io_backend import BrowserBackend
    from dbz.runner import Runner
    from dbz.state import State

    random.seed(${seed})
    State.IO_BACKEND = BrowserBackend()
    State.INTERACTIVE = True
    State.QUIET = False

    deck1 = Deck.from_spec('goku')
    deck2 = Deck.from_spec('vegeta')
    runner = Runner(deck1, deck2)
    winning_player_num = runner.run()
  `;
}

async function runGame(pyCode) {
  const pyodide = await pyodideReadyPromise;
  try {
    await pyodide.runPythonAsync(pyCode);
    const winner = pyodide.globals.get('winning_player_num');
    postMessage(JSON.stringify({type: 'done', winner}));
  } catch (err) {
    postMessage(JSON.stringify({type: 'error', message: String(err)}));
  }
}

self.onmessage = async (event) => {
  const {type} = event.data;
  const seed = event.data.seed ?? 1;

  if (type === 'init_sab') {
    controlArray = new Int32Array(event.data.controlSAB);
    textView = new Uint8Array(event.data.textSAB);
  } else if (type === 'run_cpu_vs_cpu') {
    await runGame(cpuVsCpuCode(seed));
  } else if (type === 'run_interactive') {
    await runGame(interactiveCode(seed));
  }
};
