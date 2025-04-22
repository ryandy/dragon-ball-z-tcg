import argparse
import collections
import pathlib
import random
import re
import sys

from card_factory import CardFactory
from deck import Deck
from personality_card import PersonalityCard
from player import Player
from runner import Runner
from state import State
from util import dprint


CHARACTERS = []
CARDS = []
DECK_SIZE = 10


def fetch_cards():
    global CHARACTERS, CARDS

    characters = collections.defaultdict(int)
    root_card_path = pathlib.Path(f'./cards')
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
    for card in CARDS:
        if isinstance(card, PersonalityCard):
            if (card.is_hero != deck_cards[0].is_hero
                or card.character == deck_cards[0].character
                or card.level > max_level - 2):
                continue
        card_pool.append(card)

    style_counts = collections.defaultdict(int)
    subtype_counts = collections.defaultdict(int)
    subtype_counts['Main Personality'] = max_level
    while len(deck_cards) < DECK_SIZE:
        choices = random.sample(card_pool, 3)
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
    parser = argparse.ArgumentParser(
        description='For the Collector in You! For the Gamer in You!',
        epilog='Recommended for ages 11 and up')
    parser.add_argument('-s', '--seed', type=int, default=0)
    parser.add_argument('-f', '--print-frequency', type=int, default=15)
    args = parser.parse_args()

    random.seed(args.seed)
    State.INTERACTIVE = True
    State.PRINT_FREQUENCY = args.print_frequency

    fetch_cards()
    p1 = Player(interactive=True)
    p2 = Player()

    decks = []
    for i, player in enumerate([p1, p2]):
        random.seed(args.seed + i)
        decks.append(draft_deck(player))

    runner = Runner(*decks)
    runner.run()


if __name__ == '__main__':
    main()
