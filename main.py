import random
import sys

from deck import Deck
from runner import Runner


def main():
    random.seed(0)

    deck1 = Deck.from_spec('goku')
    deck2 = Deck.from_spec('piccolo')

    runner = Runner(deck1, deck2)
    runner.run()


if __name__ == '__main__':
    main()
