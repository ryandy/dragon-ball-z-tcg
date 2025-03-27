import sys

from card import Card


class NonCombatCard(Card):
    '''Does not include drills, dragon balls, or allies'''

    def __repr__(self):
        return f'{self.name} (Non-Combat)'

    def can_be_played(self, player):
        return True

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
