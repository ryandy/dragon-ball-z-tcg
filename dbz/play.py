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
    parser.add_argument('-d', '--deck', action='append')
    parser.add_argument('-s', '--seed', type=int, default=239847938)
    parser.add_argument('-ni', '--simulate-game', action='store_true')
    parser.add_argument('-pf', '--print-frequency', type=int, default=State.PRINT_FREQUENCY)
    parser.add_argument('-pw', '--print-width', type=int, default=State.PRINT_WIDTH)
    args = parser.parse_args()

    # TODO: randomize seed by default?
    random.seed(args.seed)
    State.INTERACTIVE = not args.simulate_game
    State.PRINT_FREQUENCY = max(args.print_frequency, State.MIN_PRINT_FREQUENCY)
    State.PRINT_WIDTH = max(args.print_width, State.MIN_PRINT_WIDTH)

    deckname1 = args.deck[0] if (args.deck and len(args.deck) > 0) else 'goku'
    deckname2 = args.deck[1] if (args.deck and len(args.deck) > 1) else 'piccolo'

    deck1 = Deck.from_spec(deckname1)
    deck2 = Deck.from_spec(deckname2)

    runner = Runner(deck1, deck2)
    runner.run()


if __name__ == '__main__':
    main()
