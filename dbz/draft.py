import argparse
import collections
import pathlib
import random
import re
import sys

import numpy.random as np_random

from dbz.card_factory import CardFactory
from dbz.character import Character
from dbz.deck import Deck
from dbz.personality_card import PersonalityCard
from dbz.player import Player
from dbz.runner import Runner
from dbz.state import State
from dbz.util import dprint


CHARACTERS = []
CARDS = []
DECK_SIZE = 60


def fetch_cards():
    global CHARACTERS, CARDS

    characters = collections.defaultdict(int)
    root_card_path = pathlib.Path(__file__).parent / 'cards'
    card_paths = list(sorted(root_card_path.glob(f'**/*.py')))
    for card_path in card_paths:
        card = CardFactory.from_file(card_path)
        if card.deck_limit == 0:
            continue
        CARDS.append(card)
        if isinstance(card, PersonalityCard):
            characters[card.character] |= (1 << (card.level - 1))

    for character, value in characters.items():
        if value & 7 == 7:
            CHARACTERS.append(character)


def card_type_sort_key(card):
    val = None
    name = str(card)
    if 'Main Personality' in name:
        val = 0
    elif 'Attack' in name:
        val = 1
    elif 'Defense' in name:
        val = 2
    elif 'Non-Combat' in name:
        val = 3
    elif 'Personality' in name:
        val = 4
    return (val, name)


def draft_deck(player):
    global CHARACTERS, CARDS

    choices = random.sample(CHARACTERS, 3)
    random.shuffle(choices)
    idx = player.choose([x.name for x in choices], [''], allow_pass=False,
                        prompt='Select your Main Personality character')
    character = choices[idx]

    deck_cards = []
    for level in range(1, 6+1):
        choices = [x for x in CARDS
                   if (isinstance(x, PersonalityCard)
                       and x.character == character
                       and x.level == level)]
        if choices:
            choices = random.sample(choices, min(3, len(choices)))
            random.shuffle(choices)
            idx = player.choose([x.name for x in choices],
                                [x.card_text for x in choices],
                                allow_pass=(level > 3),
                                prompt=f'Select your Lv{level} Main Personality')
            if idx is None:
                break
            deck_cards.append(CardFactory.from_card(choices[idx]))
        else:
            break

    max_level = len(deck_cards)
    card_pool = []
    card_pool_weights = []
    for card in CARDS:
        if isinstance(card, PersonalityCard):
            if (card.is_hero != deck_cards[0].is_hero
                or card.character == character
                or card.level > max_level - 2
                or ' HT' in card.name):
                continue
        if ('heroes only' in card.card_text.lower()
            and not deck_cards[0].is_hero):
            continue
        if ('villains only' in card.card_text.lower()
            and deck_cards[0].is_hero):
            continue
        if ('villains and goku only' in card.card_text.lower()
            and not (not deck_cards[0].is_hero or character == Character.GOKU)):
            continue
        if ('saiyan heritage only' in card.card_text.lower()
            and not character.has_saiyan_heritage()):
            continue
        if ('namekian heritage only' in card.card_text.lower()
            and not character.has_namekian_heritage()):
            continue
        card_pool.append(card)
        card_pool_weights.append(card.deck_limit or 4)

    card_pool_weight = sum(card_pool_weights)
    card_pool_weights = [x / card_pool_weight for x in card_pool_weights]
    style_counts = collections.defaultdict(int)
    subtype_counts = collections.defaultdict(int)
    subtype_counts['Main Personality'] = max_level
    while len(deck_cards) < DECK_SIZE:
        choices = np_random.choice(card_pool, size=3, p=card_pool_weights, replace=False)
        random.shuffle(choices)
        idx = player.choose([str(x) for x in choices],
                            [x.card_text for x in choices],
                            allow_pass=False,
                            prompt=f'Select a card')
        card = CardFactory.from_card(choices[idx])
        subtype = re.match(r'.*\((.+)\)', str(card)).group(1)
        subtype_counts[subtype] += 1
        if card.style:
            style_counts[card.style.name.title()] += 1
        deck_cards.append(card)
        if player.interactive:
            print(f'Deck Progress: {len(deck_cards)}/{DECK_SIZE} cards')
            if style_counts:
                print(f'Card Styles:')
                for style in sorted(style_counts.keys()):
                    print(f'  {style_counts[style]}x {style}')
            print(f'Card Types:')
            for subtype in sorted(subtype_counts.keys(), key=lambda x: card_type_sort_key(x)):
                print(f'  {subtype_counts[subtype]}x {subtype}')

    return Deck(character.name.title(), deck_cards)


def main():
    global DECK_SIZE
    parser = argparse.ArgumentParser(
        description='For the Collector in You! For the Gamer in You!',
        epilog='Recommended for ages 11 and up')
    parser.add_argument('-s', '--seed', type=int, default=0)
    parser.add_argument('-f', '--print-frequency', type=int, default=State.PRINT_FREQUENCY)
    parser.add_argument('-w', '--print-width', type=int, default=State.PRINT_WIDTH)
    parser.add_argument('-i', '--interactive', action='store_true')
    parser.add_argument('-q', '--quiet', action='store_true')
    parser.add_argument('--deck-size', type=int, default=DECK_SIZE)
    parser.add_argument('--no-mpp', action='store_true')
    args = parser.parse_args()

    random.seed(args.seed)
    np_random.seed(args.seed)
    State.INTERACTIVE = args.interactive
    State.QUIET = not args.interactive and args.quiet
    State.PRINT_FREQUENCY = max(args.print_frequency, State.MIN_PRINT_FREQUENCY)
    State.PRINT_WIDTH = max(args.print_width, State.MIN_PRINT_WIDTH)
    State.ALLOW_MOST_POWERFUL_PERSONALITY_VICTORY = not args.no_mpp
    DECK_SIZE = args.deck_size

    fetch_cards()
    p1 = Player(interactive=args.interactive)
    p2 = Player()

    decks = []
    for i, player in enumerate([p1, p2]):
        random.seed(args.seed + i)
        np_random.seed(args.seed + i)
        decks.append(draft_deck(player))

    runner = Runner(*decks)
    runner.run()


if __name__ == '__main__':
    main()
