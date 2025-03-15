import abc
import sys

from character import Character
from rarity import Rarity
from saga import Saga


class Card(abc.ABC):
    def __init__(self, name, saga, card_number, rarity, character):
        self.name = name
        if isinstance(saga, str):
            saga = Saga[saga.upper()]
        self.saga = Saga(saga)
        self.card_number = card_number
        self.rarity = Rarity(rarity)
        if isinstance(character, str):
            character = Character[character.replace('-', '_').upper()]
        self.character = Character(character)
