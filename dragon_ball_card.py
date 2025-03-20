import pathlib
import sys

from card import Card
from saga import Saga
from style import Style


class DragonBallCard(Card):
    def __init__(self, name, saga, card_number, rarity, deck_limit, character, style,
                 card_text, card_power, db_set, db_number):
        super().__init__(name, saga, card_number, rarity, deck_limit, character, style,
                         card_text, card_power)
        self.db_set = db_set
        self.db_number = db_number

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
            card_module.CARD_POWER,
            card_module.DB_SET,
            card_module.DB_NUMBER)
        for card_power in card.card_powers:
            card_power.register_card(card)
        return card
