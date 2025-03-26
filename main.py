import argparse
import random
import sys

from deck import Deck
from runner import Runner
from state import State


def main():
    parser = argparse.ArgumentParser(
        description='For the Collector in You! For the Gamer in You!',
        epilog='Recommended for ages 11 and up')
    parser.add_argument('-s', '--seed', type=int, default=0)
    parser.add_argument('-f', '--print-frequency', type=int, default=15)
    parser.add_argument('-i', '--interactive', action='store_true')
    args = parser.parse_args()

    random.seed(args.seed)
    State.INTERACTIVE = args.interactive
    State.PRINT_FREQUENCY = args.print_frequency

    #deck1 = Deck.from_spec('goku')
    deck1 = Deck.from_spec('gohan')
    deck2 = Deck.from_spec('piccolo')
    runner = Runner(deck1, deck2)
    runner.run()


if __name__ == '__main__':
    main()
