import random
import sys

from card import Card


class Pile:
    '''0-index represents the bottom of the pile'''
    def __init__(self, name, cards=None):
        self.name = name
        if cards is None:
            cards = []
        self.cards = list(cards)

    def __repr__(self):
        return f'{self.name.title()}({len(self)})'

    def __len__(self):
        return len(self.cards)

    def __iter__(self):
        for card in self.cards:
            yield card

    def __add__(self, o):
        return self.cards + o.cards

    def shuffle(self):
        random.shuffle(self.cards)

    def remove_top(self):
        return self.draw()

    def remove_bottom(self):
        return self.draw_from_bottom()

    def draw(self):
        if not self.cards:
            return None
        return self._pop()

    def draw_from_bottom(self):
        if not self.cards:
            return None
        return self._pop(0)

    def remove(self, card_or_idx):
        if isinstance(card_or_idx, Card):
            idx = 0
            for idx in range(len(self)):
                if self.cards[idx] is card_or_idx:
                    break
        else:
            idx = card_or_idx
        if idx >= len(self):
            return None
        return self._pop(idx)

    def add(self, card):
        '''place card at top of pile'''
        self.add_top(card)

    def add_top(self, card):
        '''place card at top of pile'''
        self.cards.append(card)

    def add_bottom(self, card):
        '''place card at bottom of pile'''
        self.cards.insert(0, card)

    def _pop(self, idx=-1):
        return self.cards.pop(idx)
