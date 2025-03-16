import random
import sys

from deck import Deck
from state import State


def main():
    random.seed(0)

    deck1 = Deck.from_spec('goku')
    deck2 = Deck.from_spec('goku')

    state = State(deck1, deck2)
    #state.take_turn()
    state.run()


if __name__ == '__main__':
    main()
