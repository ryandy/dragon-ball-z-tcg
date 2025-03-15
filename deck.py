import pathlib
import sys

from card_factory import CardFactory
from pile import Pile
from saga import Saga


class Deck(Pile):
    def __init__(self, cards):
        super().__init__(cards)

    @classmethod
    def from_spec(cls, name):
        cards = []
        path = pathlib.Path(f'./decks/{name}'.lower())
        with open(path) as f:
            lines = f.readlines()
            for line in lines:
                tokens = line.split()
                if len(tokens) < 3:
                    continue
                count, saga, card_number = int(tokens[0]), tokens[1], int(tokens[2])
                for _ in range(count):
                    card = CardFactory.from_spec(Saga[saga.upper()], card_number)
                    cards.append(card)
        return cls(cards)
