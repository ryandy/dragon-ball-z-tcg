import random
import sys

from card import Card


class Pile:
    '''0-index represents the bottom of the pile'''
    def __init__(self, cards=None, shuffle=False):
        if cards is None:
            cards = []
        self.cards = list(cards)
        if shuffle:
            self.shuffle()

    def __len__(self):
        return len(self.cards)

    def __iter__(self):
        for card in self.cards:
            yield card

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        if not self.cards:
            return None
        return self.cards.pop()

    def remove(self, card_or_idx):
        if isinstance(card_or_idx, Card):
            for idx in range(len(self)):
                if self.cards[idx] is card_or_idx:
                    break
        else:
            idx = card_or_idx
        if idx >= len(self):
            return None
        return self.cards.pop(idx)

    def add(self, card):
        '''place card at top of pile'''
        self.add_top(card)

    def add_top(self, card):
        '''place card at top of pile'''
        self.cards.append(card)

    def add_bottom(self, card):
        '''place card at bottom of pile'''
        self.cards.insert(0, card)
