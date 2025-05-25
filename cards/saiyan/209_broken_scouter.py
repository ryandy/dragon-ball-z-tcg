import sys

from card_power_attack import CardPowerNonCombatAttack
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Non-Combat'
NAME = 'Broken Scouter'
SAGA = 'Saiyan'
CARD_NUMBER = '209'
RARITY = 5
DECK_LIMIT = None
CHARACTER = None
STYLE = None
CARD_TEXT = ('Raise your power level to full power. Remove from the game after use.')

CARD_POWER = CardPowerNonCombatAttack(
    NAME, CARD_TEXT, any_power=10, remove_from_game=True)
