import sys

from dbz.card_power_attack import CardPowerNonCombatAttack
from dbz.character import Character
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier


TYPE = 'Non-Combat'
NAME = 'A Beginner\'s Heart is Dedicated'
SAGA = 'Saiyan'
CARD_NUMBER = '191'
RARITY = 5
DECK_LIMIT = None
CHARACTER = None
STYLE = None
CARD_TEXT = ('Increase the anger of a level 1 or 2 personality by 1. Remove this card from'
             ' the game.')


class CardPowerNonCombatAttackABHID(CardPowerNonCombatAttack):
    def on_secondary_effects(self, player, phase):
        if player.main_personality.level <= 2:
            super().on_secondary_effects(player, phase)


CARD_POWER = CardPowerNonCombatAttackABHID(
    NAME, CARD_TEXT, own_anger=1, remove_from_game=True)
