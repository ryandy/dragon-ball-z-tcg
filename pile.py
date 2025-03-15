import random
import sys


class Pile:
    '''0-index represents the bottom of the pile'''
    def __init__(self, cards=None):
        if cards is None:
            cards = []
        self.cards = list(cards)

    def __len__(self):
        return len(self.cards)

    def shuffle(self):
        random.shuffle(self.cards)
