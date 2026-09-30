import itertools
import sys

import tabulate

import dbz.io_backend  # noqa: F401  (ensures State.IO_BACKEND has a default)
from dbz.state import State


def dprint(msg='', quiet=None):
    if quiet is False or State.QUIET is False:
        for line in msg.split('\n'):
            splitlines = _split_msg_by_width_and_indent(line)
            for splitline in splitlines:
                State.IO_BACKEND.write(splitline)


def card_uid(card):
    '''Per-instance id for a Card (Card.get_id() is shared by duplicate copies).
    Lets the UI match a choice option to the exact card on the board.'''
    return str(id(card))


def floating_uid(card_power):
    return f'floating-{id(card_power)}'


def ui_target(ref):
    '''Board-element uid a choice option refers to, or None if it has no
    single visible card (Pass, Declare Combat, powers with no card, ...).'''
    from dbz.card import Card
    from dbz.card_power import CardPower
    if isinstance(ref, Card):
        return card_uid(ref)
    if isinstance(ref, CardPower):
        if ref.is_floating:
            return floating_uid(ref)
        return card_uid(ref.card) if ref.card is not None else None
    return None


def _announce(player, event):
    '''Sends a structured game event to the IO backend. Opponent actions
    (CPU acting while a human is playing) block for acknowledgement when
    State.ACK_OPPONENT_ACTIONS is set. No-op for the CLI backend.'''
    event.update({
        'playerNum': player.player_num,
        'playerName': player.name,
        'isYou': bool(player.interactive),
        'round': State.ROUND_KEY,
    })
    opponent_action = (State.ACK_OPPONENT_ACTIONS
                       and not player.interactive
                       and bool(player.opponent and player.opponent.interactive))
    if State.ROUND_KEY is not None:
        # Inside a combat round: don't block per action - one ack at round end.
        if opponent_action:
            State.ROUND_NEEDS_ACK = True
        State.IO_BACKEND.announce(event, ack=False)
    else:
        State.IO_BACKEND.announce(event, ack=opponent_action)


def announce_round_end():
    '''Closes the current combat round; blocks once for an ack if the round
    contained an opponent action.'''
    event = {'type': 'round_end', 'round': State.ROUND_KEY}
    ack = State.ROUND_NEEDS_ACK
    State.ROUND_NEEDS_ACK = False
    State.IO_BACKEND.announce(event, ack=ack)


def announce_damage(player, **fields):
    '''Damage summary for `player` (the damaged player). Never blocks.'''
    event = {
        'type': 'damage',
        'playerNum': player.player_num,
        'playerName': player.name,
        'isYou': bool(player.interactive),
        'round': State.ROUND_KEY,
    }
    event.update(fields)
    State.IO_BACKEND.announce(event, ack=False)


def announce_play(player, role, name, text):
    '''role: attack | defense | shield | noncombat | ally | drill | dragon_ball | power'''
    _announce(player, {'type': 'play', 'role': role, 'name': name, 'cardText': text})


def announce_action(player, kind):
    '''kind: pass | declare_combat | skip_combat | no_defense'''
    _announce(player, {'type': 'action', 'kind': kind})


def dprint_table(table, quiet=None):
    tabulate.PRESERVE_WHITESPACE = True
    column_count = len(table)
    assert column_count >= 1

    column_width = (State.PRINT_WIDTH - (column_count + 1)) / column_count - 2
    new_table = []
    for column in range(column_count):
        # Check if columns need to be different widths
        # Note: this only works for up to 2 columns
        # Note: column0 ends up on the right - visually we want it to be the wider column
        if column == 0 and column_width % 1:
            column_width += 1
        elif column == 1 and column_width % 1:
            column_width -= 1
        new_column = []
        for cell in table[column]:
            new_cell = []
            for line in cell.split('\n'):
                splitlines = _split_msg_by_width_and_indent(line, width=int(column_width))
                #print('~~', column_width, column, splitlines)
                new_cell.extend(splitlines)
            new_column.append('\n'.join(new_cell))
        new_table.append(new_column)

    table = itertools.zip_longest(*reversed(new_table))
    table = tabulate.tabulate(table, tablefmt='fancy_grid')
    dprint(table, quiet=quiet)


def _split_msg_by_width_and_indent(msg, width=None):
    width = State.PRINT_WIDTH if width is None else width

    lines = []
    count = 0
    indent = _get_indent(msg)
    while len(msg):
        if count > 0:
            msg = f'{" " * indent}{msg}'
        cur_width = State.PRINT_WIDTH if width is None else width
        if cur_width < len(msg):
            while msg[cur_width] != ' ':
                #print('-->', cur_width, msg, len(msg))
                cur_width -= 1
        chunk = msg[:cur_width].ljust(width)
        if cur_width < len(msg) and msg[cur_width] == ' ':
            cur_width += 1
        msg = msg[cur_width:]
        lines.append(chunk)
        #print(f'chunk: "{chunk}" len={len(chunk)}')
        count += 1
    return lines or ['']


def _get_indent(s):
    idx = 0
    while idx < len(s) and (s[idx] == ' ' or s[idx] == '-'):
        idx += 1
    return idx
