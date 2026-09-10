const log = document.getElementById('log');
const board = document.getElementById('board');
const runCpuButton = document.getElementById('run-cpu');
const runInteractiveButton = document.getElementById('run-interactive');
const choicesDiv = document.getElementById('choices');
const choicesPrompt = document.getElementById('choices-prompt');
const choicesRow = document.getElementById('choices-row');

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

function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text ?? '';
  return div.innerHTML;
}

function cardHtml(card, extraClass = '') {
  return `
    <div class="card ${extraClass}" data-card-id="${escapeHtml(card.id)}">
      <div class="card-name">${escapeHtml(card.name)}</div>
      <div class="card-text">${escapeHtml(card.cardText)}</div>
    </div>`;
}

function personalityHtml(personality, extraClass = '') {
  const levelStr = personality.anger !== undefined
    ? `Lv${personality.level}.${personality.anger}`
    : `Lv${personality.level}`;
  return `
    <div class="card ${extraClass}" data-card-id="${escapeHtml(personality.id)}">
      <div class="card-name">${escapeHtml(personality.name)}
        <span class="card-stat">${levelStr} - ${escapeHtml(personality.powerAttackStr)}pwr</span>
      </div>
      <div class="card-text">${escapeHtml(personality.cardText)}</div>
    </div>`;
}

function cardBackRowHtml(count) {
  let html = '';
  for (let i = 0; i < count; i++) {
    html += '<div class="card card-back">card</div>';
  }
  return html;
}

function playerZoneHtml(player) {
  const label = player.interactive ? `You (${player.name})` : `${player.name} (CPU${player.playerNum})`;
  const counts = `Life Deck: ${player.lifeDeckCount}/${player.deckSize}`
    + ` | Discard: ${player.discardCount} | Removed: ${player.removedCount}`;

  const personalitiesHtml = personalityHtml(player.mainPersonality, 'main-personality')
    + player.allies.map((a) => personalityHtml(a)).join('');

  const handHtml = player.hand
    ? player.hand.map((c) => cardHtml(c)).join('')
    : cardBackRowHtml(player.handCount);

  const zones = [
    ['Personalities', personalitiesHtml],
    ['Hand', handHtml],
    ['Non-Combat', player.nonCombat.map((c) => cardHtml(c)).join('')],
    ['Drills', player.drills.map((c) => cardHtml(c)).join('')],
    ['Dragon Balls', player.dragonBalls.map((c) => cardHtml(c)).join('')],
  ];
  const zonesHtml = zones
    .map(([label, html]) => `
      <div class="zone-label">${label}</div>
      <div class="card-row">${html}</div>`)
    .join('');

  return `
    <div class="player-zone">
      <div class="player-header">
        <span>${escapeHtml(label)}</span>
        <span class="counts">${escapeHtml(counts)}</span>
      </div>
      ${zonesHtml}
    </div>`;
}

function renderBoard(snapshot) {
  board.innerHTML = snapshot.players.map((p) => playerZoneHtml(p)).join('');
}

function setButtonsDisabled(disabled) {
  runCpuButton.disabled = disabled;
  runInteractiveButton.disabled = disabled;
}

function submitAnswer(value) {
  const text = String(value);
  const bytes = new TextEncoder().encode(text);
  textView.set(bytes);
  Atomics.store(controlArray, CONTROL_LENGTH, bytes.length);
  Atomics.store(controlArray, CONTROL_FLAG, 1);
  Atomics.notify(controlArray, CONTROL_FLAG);

  appendLine(`>>> Choice: ${text}`);
  choicesDiv.hidden = true;
}

function choiceCardHtml(name, description, extraClass, value) {
  const valueAttr = value === undefined ? '' : ` data-value="${escapeHtml(String(value))}"`;
  return `
    <div class="card ${extraClass}"${valueAttr}>
      <div class="card-name">${escapeHtml(name)}</div>
      <div class="card-text">${escapeHtml(description)}</div>
    </div>`;
}

// payload: {prompt, names, descriptions, otherNames, otherDescriptions,
// allowPass} - Player.choose()'s own parameters (dbz/player.py), forwarded
// unchanged through BrowserBackend.read_choice. names/descriptions are
// the selectable options (1-indexed, matching what a terminal session
// would type); otherNames are shown for context but aren't choosable
// (mirrors the CLI's "/." prefix).
function renderChoices(payload) {
  choicesPrompt.textContent = payload.prompt || '';

  let html = '';
  payload.names.forEach((name, i) => {
    html += choiceCardHtml(name, payload.descriptions[i], 'selectable', i + 1);
  });
  payload.otherNames.forEach((name, i) => {
    html += choiceCardHtml(name, payload.otherDescriptions[i], 'unavailable');
  });
  if (payload.allowPass) {
    html += choiceCardHtml('Pass', 'Do nothing.', 'selectable', payload.names.length + 1);
  }
  choicesRow.innerHTML = html;

  choicesRow.querySelectorAll('.card.selectable').forEach((el) => {
    el.addEventListener('click', () => submitAnswer(el.dataset.value));
  });

  choicesDiv.hidden = false;
}

worker.onmessage = (event) => {
  const msg = JSON.parse(event.data);

  if (msg.type === 'ready') {
    setButtonsDisabled(false);
    appendLine('[Pyodide ready - dbz engine loaded]');
  } else if (msg.type === 'write') {
    appendLine(msg.line);
  } else if (msg.type === 'state') {
    renderBoard(msg.snapshot);
  } else if (msg.type === 'need_input') {
    renderChoices(msg);
  } else if (msg.type === 'done') {
    appendLine(`[Game over - player ${msg.winner} wins]`);
    choicesDiv.hidden = true;
    setButtonsDisabled(false);
  } else if (msg.type === 'error') {
    appendLine(`[Error] ${msg.message}`);
    choicesDiv.hidden = true;
    setButtonsDisabled(false);
  }
};

runCpuButton.addEventListener('click', () => {
  setButtonsDisabled(true);
  log.textContent = '';
  board.innerHTML = '';
  worker.postMessage({type: 'run_cpu_vs_cpu', seed: 1});
});

runInteractiveButton.addEventListener('click', () => {
  setButtonsDisabled(true);
  log.textContent = '';
  board.innerHTML = '';
  worker.postMessage({type: 'run_interactive', seed: 1});
});

