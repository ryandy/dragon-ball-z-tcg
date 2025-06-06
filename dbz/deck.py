import pathlib
import sys

from dbz.card_factory import CardFactory
from dbz.exception import DeckEmpty
from dbz.pile import Pile
from dbz.saga import Saga


class Deck(Pile):
    def __init__(self, name, cards):
        super().__init__(name, cards=cards)

    def _pop(self, idx=-1):
        card = super()._pop(idx) if (len(self.cards) > 0) else None
        if len(self.cards) == 0:
            raise DeckEmpty(card)
        return card

    @classmethod
    def from_spec(cls, name):
        cards = []
        path = pathlib.Path(name)
        if not path.exists():
            path = pathlib.Path(__file__).parent / 'decks' / name
        with open(path) as f:
            lines = f.readlines()
            for line in lines:
                tokens = line.split()
                if len(tokens) < 3 or tokens[0][0] == '#':
                    continue
                count, saga, card_number = int(tokens[0]), tokens[1], tokens[2]
                for _ in range(count):
                    card = CardFactory.from_spec(Saga[saga.upper()], card_number.lower())
                    cards.append(card)
        return cls(f'{name.title()}Deck', cards)

    def validate(self):
        '''
        At least 3 consecutive main personality cards
        Check for maximum number of duplicates allowed (0-4)
        Check for "saiyan heritage only"
        Check for total number of cards
        No HT personalities as allies
        No allies with level greater than MP's max minus 2
        '''
        pass
