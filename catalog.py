import argparse
import collections
import pathlib
import sys

import tabulate

from card_factory import CardFactory


def fetch_cards():
    cards = []
    characters = collections.defaultdict(int)
    root_card_path = pathlib.Path(f'./cards')
    card_paths = list(sorted(root_card_path.glob(f'**/*.py')))
    for card_path in card_paths:
        card = CardFactory.from_file(card_path)
        if card.deck_limit == 0:
            continue
        cards.append(card)
    return cards


def main():
    parser = argparse.ArgumentParser(
        description='For the Collector in You! For the Gamer in You!',
        epilog='Recommended for ages 11 and up')
    args = parser.parse_args()

    # TODO: Filtering
    # - card type
    # - basic card attribute
    # - card text substring
    # - damage/damage_modifier attributes
    # - cost attributes
    #attr = 'remove_from_game'
    attr = 'own_anger'
    cards = fetch_cards()
    cards.sort(key=lambda x: (x.__class__.__name__, x.saga.value, x.card_number))
    table = []
    for card in cards:
        for card_power in card.card_powers:
            if hasattr(card_power, attr) and getattr(card_power, attr):
                table.append([card.name,
                              card.__class__.__name__.replace("Card", ""),
                              card_power.__class__.__name__.replace("CardPower", ""),
                              getattr(card_power, attr)])
                #print(f'{card.name}'
                #      f', {card.__class__.__name__.replace("Card", "")}'
                #      f', {card_power.__class__.__name__.replace("CardPower", "")}'
                #      f', {getattr(card_power, attr)}')
    print(tabulate.tabulate(table))


if __name__ == '__main__':
    main()
