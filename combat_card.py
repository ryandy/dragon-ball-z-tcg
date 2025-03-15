import pathlib
import sys

from card import Card
from saga import Saga
from style import Style


class CombatCard(Card):
    def __init__(self, name, saga, card_number, rarity, character,
                 style, is_physical, is_attack, card_power):
        super().__init__(name, saga, card_number, rarity, character)
        if isinstance(style, str):
            style = Style[style.upper()]
        self.style = Style(style)
        self.is_physical = is_physical
        self.is_attack = is_attack
        self.card_power = card_power

    def __repr__(self):
        desc1 = 'Physical' if self.is_physical else 'Energy'
        desc2 = 'Attack' if self.is_attack else 'Defense'
        return f'{self.name} ({desc1} {desc2})'

    @classmethod
    def from_spec(cls, card_module):
        return cls(
            card_module.NAME,
            card_module.SAGA,
            card_module.CARD_NUMBER,
            card_module.RARITY,
            card_module.CHARACTER,
            card_module.STYLE,
            card_module.IS_PHYSICAL,
            card_module.IS_ATTACK,
            card_module.CARD_POWER)
