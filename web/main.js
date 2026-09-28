const log = document.getElementById('log');
const board = document.getElementById('board');
const status = document.getElementById('status');
const setupDiv = document.getElementById('setup');
const seedInput = document.getElementById('seed-input');
const deck1Select = document.getElementById('deck1-select');
const deck2Select = document.getElementById('deck2-select');
const startGameButton = document.getElementById('start-game');
const choicesDiv = document.getElementById('choices');
const choicesPrompt = document.getElementById('choices-prompt');
const choicesRow = document.getElementById('choices-row');
const pileViewerBackdrop = document.getElementById('pile-viewer-backdrop');
const pileViewerTitle = document.getElementById('pile-viewer-title');
const pileViewerRow = document.getElementById('pile-viewer-row');
const pileViewerClose = document.getElementById('pile-viewer-close');

// Fixed starting point for reproducible playtesting.
const DEFAULT_SEED = 1;
const DEFAULT_DECK1 = 'goku_survival';
const DEFAULT_DECK2 = 'vegeta_db';

// Cache-bust: Chromium caches `type: 'module'` worker scripts (and their
// static imports) separately from the regular HTTP cache, in a way that
// can survive across navigations even with Cache-Control: no-store. A
// unique query string forces a genuinely fresh fetch on every page load.
const worker = new Worker(`worker.js?v=${Date.now()}`, {type: 'module'});

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

seedInput.value = DEFAULT_SEED;

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

function pileLinkHtml(player, pile, count) {
  const label = pile === 'discard' ? 'Discard' : 'Removed';
  return `<span class="pile-link" data-player-num="${player.playerNum}" data-pile="${pile}">${label}: ${count}</span>`;
}

function playerZoneHtml(player) {
  const label = player.interactive ? `You (${player.name})` : `${player.name} (CPU${player.playerNum})`;
  const counts = `Life Deck: ${player.lifeDeckCount}/${player.deckSize} | `
    + pileLinkHtml(player, 'discard', player.discardCount) + ' | '
    + pileLinkHtml(player, 'removed', player.removedCount);

  const personalitiesHtml = personalityHtml(player.mainPersonality, 'main-personality')
    + player.allies.map((a) => personalityHtml(a)).join('');

  const handHtml = player.hand
    ? player.hand.map((c) => cardHtml(c)).join('')
    : cardBackRowHtml(player.handCount);

  const zones = [
    ['Personalities', personalitiesHtml],
    ['Hand', handHtml],
    ['Non-Combat', player.nonCombat.map((c) => cardHtml(c)).join('')],
    ['Active Effects', player.floatingCardPowers.map((c) => cardHtml(c, 'floating-effect')).join('')],
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
        <span class="counts">${counts}</span>
      </div>
      ${zonesHtml}
    </div>`;
}

let latestSnapshot = null;

function renderBoard(snapshot) {
  latestSnapshot = snapshot;
  board.innerHTML = snapshot.players.map((p) => playerZoneHtml(p)).join('');

  const phase = snapshot.phase ?? 'Starting';
  status.textContent = `Turn ${snapshot.turn} | Phase: ${phase} | Seed: ${snapshot.seed}`;
  status.hidden = false;

  if (!pileViewerBackdrop.hidden) {
    renderPileViewer(pileViewerBackdrop.dataset.playerNum, pileViewerBackdrop.dataset.pile);
  }
}

function renderPileViewer(playerNum, pile) {
  const player = latestSnapshot.players.find((p) => String(p.playerNum) === String(playerNum));
  if (!player) {
    pileViewerBackdrop.hidden = true;
    return;
  }
  const label = player.interactive ? `You (${player.name})` : `${player.name} (CPU${player.playerNum})`;
  const cards = pile === 'discard' ? player.discardCards : player.removedCards;
  const pileLabel = pile === 'discard' ? 'Discard' : 'Removed';

  pileViewerBackdrop.dataset.playerNum = playerNum;
  pileViewerBackdrop.dataset.pile = pile;
  pileViewerTitle.textContent = `${label} - ${pileLabel} Pile (${cards.length})`;
  pileViewerRow.innerHTML = cards.length
    ? cards.map((c) => cardHtml(c)).join('')
    : '<span>(empty)</span>';
}

function openPileViewer(playerNum, pile) {
  renderPileViewer(playerNum, pile);
  pileViewerBackdrop.hidden = false;
}

function closePileViewer() {
  pileViewerBackdrop.hidden = true;
}

board.addEventListener('click', (event) => {
  const link = event.target.closest('.pile-link');
  if (link) {
    openPileViewer(link.dataset.playerNum, link.dataset.pile);
  }
});

pileViewerClose.addEventListener('click', closePileViewer);

pileViewerBackdrop.addEventListener('click', (event) => {
  if (event.target === pileViewerBackdrop) {
    closePileViewer();
  }
});

document.addEventListener('keydown', (event) => {
  if (event.key === 'Escape' && !pileViewerBackdrop.hidden) {
    closePileViewer();
  }
});

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

function populateDeckSelects(deckNames) {
  const optionsHtml = deckNames.map((name) => `<option value="${escapeHtml(name)}">${escapeHtml(name)}</option>`).join('');
  deck1Select.innerHTML = optionsHtml;
  deck2Select.innerHTML = optionsHtml;
  deck1Select.value = deckNames.includes(DEFAULT_DECK1) ? DEFAULT_DECK1 : deckNames[0];
  deck2Select.value = deckNames.includes(DEFAULT_DECK2) ? DEFAULT_DECK2 : (deckNames[1] ?? deckNames[0]);
}

function showSetup() {
  seedInput.value = DEFAULT_SEED;
  setupDiv.hidden = false;
  status.hidden = true;
}

worker.onmessage = (event) => {
  const msg = JSON.parse(event.data);

  if (msg.type === 'ready') {
    populateDeckSelects(msg.decks);
    deck1Select.disabled = false;
    deck2Select.disabled = false;
    startGameButton.disabled = false;
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
    showSetup();
  } else if (msg.type === 'error') {
    appendLine(`[Error] ${msg.message}`);
    choicesDiv.hidden = true;
    showSetup();
  }
};

startGameButton.addEventListener('click', () => {
  const seed = parseInt(seedInput.value, 10) || DEFAULT_SEED;
  const deck1 = deck1Select.value;
  const deck2 = deck2Select.value;

  setupDiv.hidden = true;
  log.textContent = '';
  board.innerHTML = '';
  worker.postMessage({type: 'run_interactive', seed, deck1, deck2});
});

