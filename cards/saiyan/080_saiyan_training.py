import sys

from card_power_attack import CardPowerNonCombatAttack
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


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


class CardPowerNonCombatAttackST(CardPowerNonCombatAttack):
    def is_restricted(self, player):
        if (player.control_personality.is_hero
            and player.character != Character.GOKU):
            return True
        return super().is_restricted(player)


CARD_POWER = CardPowerNonCombatAttackST(NAME, CARD_TEXT, rejuvenate_choice_count=2)
