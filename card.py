import abc
import sys

from character import Character
from rarity import Rarity
from saga import Saga


class Card(abc.ABC):
    def __init__(self, name, saga, card_number, rarity, character, card_text,
                 card_power_condition, card_power):
        self.name = name
        if isinstance(saga, str):
            saga = Saga[saga.upper()]
        self.saga = Saga(saga)
        self.card_number = card_number
        self.rarity = Rarity(rarity)
        if isinstance(character, str):
            character = Character[character.replace('-', '_').upper()]
        self.character = Character(character)
        self.card_text = card_text
        self.card_power_condition = card_power_condition
        self.card_power = card_power

    @abc.abstractmethod
    def get_description(self, detailed=False):
        pass
