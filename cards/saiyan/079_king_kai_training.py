import sys

from card_power_attack import CardPowerNonCombatAttack
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier
from util import dprint


TYPE = 'Non-Combat'
NAME = 'King Kai Training'
SAGA = 'Saiyan'
CARD_NUMBER = '79'
RARITY = 3
DECK_LIMIT = None
CHARACTER = None
STYLE = None
CARD_TEXT = ('Heroes only. Choose 2 cards from your discard pile and place them on'
             ' the bottom of your Life Deck.')


class CardPowerKKT(CardPowerNonCombatAttack):
    def on_secondary_effects(self, player, phase):
        super().on_secondary_effects(player, phase)
        for _ in range(2):
            card = player.choose_discard_pile_card()
            if card:
                if player.interactive:
                    dprint(f'{player} returns {card} to their life deck')
                else:
                    dprint(f'{player} returns a card to their life deck')
                player.discard_pile.remove(card)
                player.life_deck.add_bottom(card)
                card.set_pile(player.life_deck)


CARD_POWER = CardPowerKKT(NAME, CARD_TEXT, heroes_only=True)
