import pathlib
import sys

from card import Card
from saga import Saga
from style import Style


class CombatCard(Card):
    def __init__(self, name, saga, card_number, rarity, character, card_text, card_power,
                 subtype, style):
        super().__init__(name, saga, card_number, rarity, character, card_text, card_power)
        self.subtype = subtype
        if isinstance(style, str):
            style = Style[style.upper()]
        self.style = Style(style)

    def __repr__(self):
        return f'{self.name} ({self.subtype})'

    def get_description(self, detailed=False):
        description = f'{self.name} - {self.subtype}'
        if not detailed:
            return description
        description = f'{description}\n  {self.card_text}'
        return description

    @classmethod
    def from_spec(cls, card_module):
        card = cls(
            card_module.NAME,
            card_module.SAGA,
            card_module.CARD_NUMBER,
            card_module.RARITY,
            card_module.CHARACTER,
            card_module.CARD_TEXT,
            card_module.CARD_POWER,
            card_module.SUBTYPE,
            card_module.STYLE)
        for card_power in card.card_powers:
            card_power.register_card(card)
        return card
