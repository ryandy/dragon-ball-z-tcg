import argparse
import random
import sys

from dbz.deck import Deck
from dbz.runner import Runner
from dbz.state import State


def main():
    parser = argparse.ArgumentParser(
        description='For the Collector in You! For the Gamer in You!',
        epilog='Recommended for ages 11 and up')
    parser.add_argument('-s', '--seed', type=int, default=0)
    parser.add_argument('-f', '--print-frequency', type=int, default=15)
    parser.add_argument('-i', '--interactive', action='store_true')
    parser.add_argument('-d', '--deck', action='append')
    args = parser.parse_args()

    random.seed(args.seed)
    State.INTERACTIVE = args.interactive
    State.PRINT_FREQUENCY = args.print_frequency

    deckname1 = args.deck[0] if len(args.deck) > 0 else 'goku'
    deckname2 = args.deck[1] if len(args.deck) > 1 else 'piccolo'

    deck1 = Deck.from_spec(deckname1)
    deck2 = Deck.from_spec(deckname2)

    runner = Runner(deck1, deck2)
    runner.run()


if __name__ == '__main__':
    main()
