import abc
import sys

from character import Character
from rarity import Rarity
from saga import Saga


class Card(abc.ABC):
    def __init__(self, name, saga, card_number, rarity, character, card_text, card_power):
        self.name = name
        if isinstance(saga, str):
            saga = Saga[saga.upper()]
        self.saga = Saga(saga)
        self.card_number = card_number
        self.rarity = Rarity(rarity)
        if isinstance(character, str):
            character = Character[character.replace('-', '_').upper()]
        self.character = Character(character) if character else None
        self.card_text = card_text
        if isinstance(card_power, list):
            self.card_powers = card_power
        else:
            self.card_powers = [card_power]

    @abc.abstractmethod
    def get_description(self, detailed=False):
        pass
