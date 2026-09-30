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
const historyList = document.getElementById('history');
const logDetails = document.getElementById('log-details');

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
    <div class="card ${extraClass}" data-card-id="${escapeHtml(card.id)}" data-uid="${escapeHtml(card.uid)}">
      <div class="card-name">${escapeHtml(card.name)}</div>
      <div class="card-text">${escapeHtml(card.cardText)}</div>
    </div>`;
}

function personalityHtml(personality, extraClass = '') {
  const levelStr = personality.anger !== undefined
    ? `Lv${personality.level}.${personality.anger}`
    : `Lv${personality.level}`;
  return `
    <div class="card ${extraClass}" data-card-id="${escapeHtml(personality.id)}" data-uid="${escapeHtml(personality.uid)}">
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
// The stage between the player zones shows the current combat round as a
// growing row of "beats" (attack -> defense -> damage). Events outside a round
// (round == null) are single-beat strips. The row is cleared when the first
// event of the next round arrives.
let stageBeats = [];
let stageRound = null;   // round key of stageBeats (null = single-beat strip)
let stageAcked = false;  // the player has pressed Continue for this strip
let lastEvent = null;    // most recent event, including round_end
let pendingAck = false;  // true while the engine is blocked waiting for "Continue"

const PLAY_VERBS = {
  attack: 'attacks with',
  defense: 'defends with',
  shield: 'activates Defense Shield',
  noncombat: 'uses',
  ally: 'plays ally',
  drill: 'plays drill',
  dragon_ball: 'plays Dragon Ball',
  power: 'uses',
};
const ACTION_TEXT = {
  pass: 'passes',
  declare_combat: 'declares combat!',
  skip_combat: 'skips combat',
  no_defense: 'has no defense',
};

// "attacks with" -> "attack with", "has no defense" -> "have no defense"
function secondPerson(phrase) {
  const [verb, ...rest] = phrase.split(' ');
  let base = verb.replace(/s$/, '');
  if (verb === 'has') {
    base = 'have';
  } else if (verb.endsWith('sses')) {
    base = verb.slice(0, -2);
  }
  return [base, ...rest].join(' ');
}

function eventText(ev) {
  const actor = ev.isYou ? 'You' : ev.playerName;
  const verbPhrase = ev.type === 'play'
    ? (PLAY_VERBS[ev.role] ?? 'plays')
    : (ACTION_TEXT[ev.kind] ?? ev.kind);
  return `${actor} ${ev.isYou ? secondPerson(verbPhrase) : verbPhrase}`;
}

function damageSummary(ev) {
  if (ev.stopped) {
    return 'Attack stopped';
  }
  const parts = [];
  if (ev.powerDamage) {
    parts.push(`${ev.powerDamage} power`);
  }
  if (ev.lifeDamage) {
    parts.push(`${ev.lifeDamage} life card${ev.lifeDamage === 1 ? '' : 's'}`);
  }
  const verb = ev.isYou ? 'take' : 'takes';
  return parts.length ? `${verb} ${parts.join(' + ')}` : `${verb} no damage`;
}

function damageLine(ev) {
  const who = ev.isYou ? 'You' : ev.playerName;
  return ev.stopped ? `${who}: attack stopped` : `${who} ${damageSummary(ev)}`;
}

function addHistory(ev) {
  const turn = latestSnapshot ? `T${latestSnapshot.turn}: ` : '';
  const li = document.createElement('li');
  li.className = ev.isYou ? 'you' : 'opponent';
  if (ev.type === 'damage') {
    li.textContent = `${turn}${damageLine(ev)}`;
  } else {
    const card = ev.type === 'play' ? ` ${ev.name}` : '';
    li.textContent = `${turn}${eventText(ev)}${card}`;
  }
  historyList.prepend(li);
}

function damageBeatHtml(ev) {
  const who = ev.isYou ? 'You' : ev.playerName;
  let body = '';
  if (ev.stopped) {
    body = '<div class="card-text">No damage.</div>';
  } else {
    if (ev.target) {
      body += `<div class="card-text">${escapeHtml(ev.target.name)} Lv${ev.target.level}: `
        + `${escapeHtml(ev.target.powerBefore)} &rarr; ${escapeHtml(ev.target.powerAfter)}pwr</div>`;
    }
    (ev.lifeCards ?? []).forEach((c) => {
      body += `<div class="card-text">&minus; ${escapeHtml(c.name)}</div>`;
    });
    if (ev.drawn) {
      body += `<div class="card-text">+${ev.drawn} card${ev.drawn === 1 ? '' : 's'} drawn</div>`;
    }
    if (ev.stolen) {
      body += '<div class="card-text">Dragon Ball stolen!</div>';
    }
  }
  return `
    <div class="stage-beat">
      <div class="stage-text">${escapeHtml(who)} ${ev.stopped ? '' : escapeHtml(damageSummary(ev))}</div>
      <div class="card damage-beat">
        <div class="card-name">${ev.stopped ? 'Attack stopped' : 'Damage'}</div>
        ${body}
      </div>
    </div>`;
}

function beatHtml(ev) {
  if (ev.type === 'damage') {
    return damageBeatHtml(ev);
  }
  const cardPart = ev.type === 'play'
    ? cardHtml({id: `stage-${ev.name}`, name: ev.name, cardText: ev.cardText})
    : '';
  return `
    <div class="stage-beat">
      <div class="stage-text">${escapeHtml(eventText(ev))}</div>
      ${cardPart}
    </div>`;
}

function stageHtml() {
  if (stageBeats.length === 0) {
    return '';
  }
  const opponentInvolved = stageBeats.some((ev) => !ev.isYou);
  const cls = `stage ${opponentInvolved ? 'opponent' : 'you'}${stageAcked ? ' acked' : ''}`;
  return `
    <div class="${cls}">
      ${stageBeats.map((ev) => beatHtml(ev)).join('<div class="stage-arrow">&rarr;</div>')}
    </div>`;
}

function renderBoard(snapshot) {
  latestSnapshot = snapshot;
  const zones = snapshot.players.map((p) => playerZoneHtml(p));
  board.innerHTML = zones[0] + stageHtml() + zones.slice(1).join('');

  const phase = snapshot.phase ?? 'Starting';
  status.textContent = `Turn ${snapshot.turn} | Phase: ${phase} | Seed: ${snapshot.seed}`;
  status.hidden = false;

  applyChoiceToBoard();

  if (!pileViewerBackdrop.hidden) {
    renderPileViewer(pileViewerBackdrop.dataset.playerNum, pileViewerBackdrop.dataset.pile);
  }
}

// The pending choice (payload from BrowserBackend.read_choice), or null.
let activeChoice = null;

function boardCardByUid(uid) {
  return uid ? board.querySelector(`.card[data-uid="${CSS.escape(String(uid))}"]`) : null;
}

// Options whose target card is visible on the board (and unambiguous - no
// other option points at the same card) are answered by clicking that card.
// Everything else stays in the bottom row.
function onBoardOptionIndexes(payload) {
  const counts = {};
  payload.targets.forEach((t) => { if (t) counts[t] = (counts[t] ?? 0) + 1; });
  const indexes = new Set();
  payload.targets.forEach((t, i) => {
    if (t && counts[t] === 1 && boardCardByUid(t)) {
      indexes.add(i);
    }
  });
  return indexes;
}

function clearChoiceFromBoard() {
  board.querySelectorAll('.card.selectable, .card.unavailable').forEach((el) => {
    el.classList.remove('selectable', 'unavailable');
    delete el.dataset.value;
  });
}

function applyChoiceToBoard() {
  clearChoiceFromBoard();
  if (!activeChoice) {
    return;
  }
  onBoardOptionIndexes(activeChoice).forEach((i) => {
    const el = boardCardByUid(activeChoice.targets[i]);
    el.classList.add('selectable');
    el.dataset.value = String(i + 1);
  });
  (activeChoice.otherTargets ?? []).forEach((t) => {
    boardCardByUid(t)?.classList.add('unavailable');
  });
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
  const chosen = event.target.closest('.card.selectable[data-value]');
  if (chosen && activeChoice) {
    submitAnswer(chosen.dataset.value);
  }
});

// Shows "Continue" as a normal choice card (same look/place as "Pass") so an
// ack feels like any other decision.
function renderAckChoice() {
  activeChoice = null;
  clearChoiceFromBoard();
  const ev = lastEvent;
  if (!ev) {
    choicesPrompt.textContent = '';
  } else if (ev.type === 'round_end') {
    choicesPrompt.textContent = 'Round complete';
  } else if (ev.type === 'damage') {
    choicesPrompt.textContent = damageLine(ev);
  } else {
    choicesPrompt.textContent = `${eventText(ev)}${ev.type === 'play' ? ` ${ev.name}` : ''}`;
  }
  choicesRow.innerHTML = choiceCardHtml('Continue', '', 'selectable', 1);
  choicesRow.querySelector('.card.selectable').addEventListener('click', acknowledge);
  choicesDiv.hidden = false;
}

function acknowledge() {
  if (!pendingAck) {
    return;
  }
  pendingAck = false;
  stageAcked = true;
  sendAnswer('1');
  choicesDiv.hidden = true;
  activeChoice = null;
  if (latestSnapshot) {
    renderBoard(latestSnapshot);
  }
}

pileViewerClose.addEventListener('click', closePileViewer);

pileViewerBackdrop.addEventListener('click', (event) => {
  if (event.target === pileViewerBackdrop) {
    closePileViewer();
  }
});

document.addEventListener('keydown', (event) => {
  if (event.key === 'Escape' && !pileViewerBackdrop.hidden) {
    closePileViewer();
  } else if ((event.key === 'Enter' || event.key === ' ')
             && pendingAck && pileViewerBackdrop.hidden) {
    event.preventDefault();
    acknowledge();
  }
});

// Wakes the worker thread blocked in dbzReadChoice with the given answer text.
function sendAnswer(value) {
  const bytes = new TextEncoder().encode(String(value));
  textView.set(bytes);
  Atomics.store(controlArray, CONTROL_LENGTH, bytes.length);
  Atomics.store(controlArray, CONTROL_FLAG, 1);
  Atomics.notify(controlArray, CONTROL_FLAG);
}

function submitAnswer(value) {
  sendAnswer(value);
  appendLine(`>>> Choice: ${value}`);
  choicesDiv.hidden = true;
  activeChoice = null;
  clearChoiceFromBoard();
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
// would type). targets are board-card uids for on-board selection (see
// applyChoiceToBoard); otherNames are unplayable hand cards, dimmed on the board.
function renderChoices(payload) {
  choicesPrompt.textContent = payload.prompt || '';

  activeChoice = payload;
  const onBoard = onBoardOptionIndexes(payload);

  let html = '';
  payload.names.forEach((name, i) => {
    if (!onBoard.has(i)) {
      html += choiceCardHtml(name, payload.descriptions[i], 'selectable', i + 1);
    }
  });
  if (payload.allowPass) {
    html += choiceCardHtml('Pass', 'Do nothing.', 'selectable', payload.names.length + 1);
  }
  choicesRow.innerHTML = html;

  choicesRow.querySelectorAll('.card.selectable').forEach((el) => {
    el.addEventListener('click', () => submitAnswer(el.dataset.value));
  });

  choicesDiv.hidden = false;
  applyChoiceToBoard();
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
  } else if (msg.type === 'event') {
    const ev = {...msg.event, ack: msg.ack};
    lastEvent = ev;
    if (ev.type !== 'round_end') {
      if (ev.round == null || ev.round !== stageRound) {
        stageBeats = [];
        stageAcked = false;
      }
      stageRound = ev.round ?? null;
      stageBeats.push(ev);
      addHistory(ev);
    }
    if (latestSnapshot) {
      renderBoard(latestSnapshot);
    }
  } else if (msg.type === 'need_input' && msg.kind === 'ack') {
    pendingAck = true;
    renderAckChoice();
    if (latestSnapshot) {
      renderBoard(latestSnapshot);
    }
  } else if (msg.type === 'need_input') {
    renderChoices(msg);
  } else if (msg.type === 'done') {
    appendLine(`[Game over - player ${msg.winner} wins]`);
    choicesDiv.hidden = true;
    showSetup();
  } else if (msg.type === 'error') {
    appendLine(`[Error] ${msg.message}`);
    logDetails.open = true;
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
  stageBeats = [];
  stageRound = null;
  stageAcked = false;
  lastEvent = null;
  pendingAck = false;
  activeChoice = null;
  historyList.innerHTML = '';
  worker.postMessage({type: 'run_interactive', seed, deck1, deck2});
});

