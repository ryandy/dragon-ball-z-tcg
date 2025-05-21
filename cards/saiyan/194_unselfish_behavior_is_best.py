import sys

from card_power_attack import CardPowerNonCombatAttack
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Non-Combat'
NAME = 'Unselfish Behavior is Best'
SAGA = 'Saiyan'
CARD_NUMBER = '194'
RARITY = 5
DECK_LIMIT = None
CHARACTER = None
STYLE = None
CARD_TEXT = ('The efforts of your allies stop this combat. You must have an ally out on the'
             ' table to use this card. Remove from the game after use.')


class CardPowerNonCombatAttackUBIB(CardPowerNonCombatAttack):
    def is_restricted(self, player):
        if len(player.allies) == 0:
            return True
        return super().is_restricted(player)


CARD_POWER = CardPowerNonCombatAttack(
    NAME, CARD_TEXT, force_end_combat=True, remove_from_game=True)
