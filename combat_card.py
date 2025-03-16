import pathlib
import sys

from card import Card
from saga import Saga
from style import Style


class CombatCard(Card):
    def __init__(self, name, saga, card_number, rarity, character, card_text,
                 style, is_physical, is_attack, card_power_condition, card_power):
        super().__init__(name, saga, card_number, rarity, character, card_text,
                         card_power_condition, card_power)
        if isinstance(style, str):
            style = Style[style.upper()]
        self.style = Style(style)
        self.is_physical = is_physical
        self.is_attack = is_attack

    def __repr__(self):
        desc1 = 'Physical' if self.is_physical else 'Energy'
        desc2 = 'Attack' if self.is_attack else 'Defense'
        return f'{self.name} ({desc1} {desc2})'

    def get_description(self, detailed=False):
        desc1 = 'Physical' if self.is_physical else 'Energy'
        desc2 = 'Attack' if self.is_attack else 'Defense'
        description = f'{self.name} - Combat: {desc1} {desc2}'
        if not detailed:
            return description
        description = f'{description}\n  {self.card_text}'
        return description

    @classmethod
    def from_spec(cls, card_module):
        return cls(
            card_module.NAME,
            card_module.SAGA,
            card_module.CARD_NUMBER,
            card_module.RARITY,
            card_module.CHARACTER,
            card_module.CARD_TEXT,
            card_module.STYLE,
            card_module.IS_PHYSICAL,
            card_module.IS_ATTACK,
            card_module.CARD_POWER_CONDITION,
            card_module.CARD_POWER)
