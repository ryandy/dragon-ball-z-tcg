import argparse
import collections
import pathlib
import sys

import tabulate
import textwrap

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
    cards.sort(key=lambda x: (x.__class__.__name__, x.saga.value, x.card_number.zfill(3)))
    return cards


def main():
    parser = argparse.ArgumentParser(
        description='For the Collector in You! For the Gamer in You!',
        epilog='Recommended for ages 11 and up')
    parser.add_argument('--card_type', '--card-type')
    parser.add_argument('--power_type', '--power-type')
    parser.add_argument('--text')
    parser.add_argument('--attr')
    args = parser.parse_args()

    # TODO: Filtering
    # - damage/damage_modifier attributes
    # - cost attributes

    cards = fetch_cards()
    table = []
    for card in cards:
        for card_power in card.card_powers:
            if (True
                and (not args.card_type
                     or args.card_type.lower() in card.__class__.__name__.lower())
                and (not args.power_type
                     or args.power_type.lower() in card_power.__class__.__name__.lower())
                and (not args.attr
                     or (hasattr(card_power, args.attr) and getattr(card_power, args.attr))
                     or (hasattr(card, args.attr) and getattr(card, args.attr)))
                and (not args.text
                     or args.text.lower() in card_power.description.lower()
                     or args.text.lower() in str(card).lower())):
                row = [card.get_id(),
                       card.name,
                       card.__class__.__name__.replace("Card", ""),
                       card_power.__class__.__name__.replace("CardPower", "")]
                if args.attr:
                    val = (getattr(card, args.attr)
                           if hasattr(card, args.attr) else
                           getattr(card_power, args.attr))
                    row.append(val)
                row.append('\n'.join(textwrap.wrap(card_power.description, width=80)))
                table.append(row)
    if args.attr:
        table.sort(key=lambda x: (
            x[4],  # attr
            x[2],  # card.class.name
            x[0],  # card saga/number
            ))
    print(tabulate.tabulate(table))


if __name__ == '__main__':
    main()
