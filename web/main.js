const log = document.getElementById('log');
const runCpuButton = document.getElementById('run-cpu');
const runInteractiveButton = document.getElementById('run-interactive');
const inputRow = document.getElementById('input-row');
const inputPromptLabel = document.getElementById('input-prompt-label');
const choiceInput = document.getElementById('choice-input');
const submitButton = document.getElementById('submit-choice');

const worker = new Worker('worker.js', {type: 'module'});

// Shared buffers for the synchronous input bridge (see
// dbz/io_backend.py's BrowserBackend.read_choice and worker.js's
// dbzReadChoice). controlArray[0] is the Atomics.wait/notify flag;
// controlArray[1] is the byte length of the UTF-8 answer written into
// textView by submitAnswer().
const CONTROL_FLAG = 0;
const CONTROL_LENGTH = 1;
const controlSAB = new SharedArrayBuffer(8);
const controlArray = new Int32Array(controlSAB);
const textSAB = new SharedArrayBuffer(1024);
const textView = new Uint8Array(textSAB);

worker.postMessage({type: 'init_sab', controlSAB, textSAB});

function appendLine(text) {
  log.textContent += text + '\n';
  log.scrollTop = log.scrollHeight;
}

function setButtonsDisabled(disabled) {
  runCpuButton.disabled = disabled;
  runInteractiveButton.disabled = disabled;
}

function submitAnswer() {
  const text = choiceInput.value;
  const bytes = new TextEncoder().encode(text);
  textView.set(bytes);
  Atomics.store(controlArray, CONTROL_LENGTH, bytes.length);
  Atomics.store(controlArray, CONTROL_FLAG, 1);
  Atomics.notify(controlArray, CONTROL_FLAG);

  appendLine(`>>> Choice: ${text}`);
  inputRow.hidden = true;
  choiceInput.value = '';
}

worker.onmessage = (event) => {
  const msg = JSON.parse(event.data);

  if (msg.type === 'ready') {
    setButtonsDisabled(false);
    appendLine('[Pyodide ready - dbz engine loaded]');
  } else if (msg.type === 'write') {
    appendLine(msg.line);
  } else if (msg.type === 'need_input') {
    inputPromptLabel.textContent = msg.prompt;
    inputRow.hidden = false;
    choiceInput.focus();
  } else if (msg.type === 'done') {
    appendLine(`[Game over - player ${msg.winner} wins]`);
    inputRow.hidden = true;
    setButtonsDisabled(false);
  } else if (msg.type === 'error') {
    appendLine(`[Error] ${msg.message}`);
    inputRow.hidden = true;
    setButtonsDisabled(false);
  }
};

runCpuButton.addEventListener('click', () => {
  setButtonsDisabled(true);
  log.textContent = '';
  worker.postMessage({type: 'run_cpu_vs_cpu', seed: 1});
});

runInteractiveButton.addEventListener('click', () => {
  setButtonsDisabled(true);
  log.textContent = '';
  worker.postMessage({type: 'run_interactive', seed: 1});
});

submitButton.addEventListener('click', submitAnswer);
choiceInput.addEventListener('keydown', (event) => {
  if (event.key === 'Enter') {
    submitAnswer();
  }
});
