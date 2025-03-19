import pathlib
import sys

from card import Card
from saga import Saga
from style import Style


class NonCombatCard(Card):
    '''Does not include drills, dragon balls, or allies'''

    def get_description(self, detailed=False):
        description = f'{self.name}'
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
            card_module.DECK_LIMIT,
            card_module.CHARACTER,
            card_module.STYLE,
            card_module.CARD_TEXT,
            card_module.CARD_POWER)
        for card_power in card.card_powers:
            card_power.register_card(card)
        return card
