import sys

from dbz.card import Card
from dbz.saga import Saga
from dbz.style import Style


class DragonBallCard(Card):
    def __init__(self, name, saga, card_number, rarity, deck_limit, character, style,
                 card_text, card_power, db_set, db_number):
        super().__init__(name, saga, card_number, rarity, deck_limit, character, style,
                         card_text, card_power)
        self.db_set = db_set
        self.db_number = db_number

    def __repr__(self):
        return f'{self.name} (Non-Combat)'

    def is_duplicate(self, other_card):
        return (isinstance(other_card, DragonBallCard)
                and self.db_set == other_card.db_set
                and self.db_number == other_card.db_number)

    def can_be_played(self, player):
        # Only 1 of each Dragon Ball set/number can be on the table at a time
        dup_restricted = any(self.is_duplicate(x)
                             for x in player.dragon_balls + player.opponent.dragon_balls)
        return not dup_restricted

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
