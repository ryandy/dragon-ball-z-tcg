import sys

from card_power_attack import CardPowerNonCombatAttack
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier
from util import dprint


TYPE = 'Non-Combat'
NAME = 'Saiyan Training'
SAGA = 'Saiyan'
CARD_NUMBER = '80'
RARITY = 3
DECK_LIMIT = None
CHARACTER = None
STYLE = 'Saiyan'
CARD_TEXT = ('Villains and Goku only. Choose 2 cards from your discard pile and place them'
             ' on the bottom of your Life Deck.')


class CardPowerST(CardPowerNonCombatAttack):
    def is_restricted(self, player):
        if (player.control_personality.is_hero
            and player.character != Character.GOKU):
            return True
        return super().is_restricted(player)

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


CARD_POWER = CardPowerST(NAME, CARD_TEXT)
