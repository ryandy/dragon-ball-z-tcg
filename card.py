import abc
import sys


class Card(abc.ABC):
    def __init__(self, name, saga, card_number, rarity, character):
        self.name = name
        self.saga = saga
        self.card_number = card_number
        self.rarity = rarity
        self.character = character
