import sys

from card_power_attack import CardPowerNonCombatAttack
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Non-Combat'
NAME = 'Power Up More!'
SAGA = 'Saiyan'
CARD_NUMBER = '97'
RARITY = 3
DECK_LIMIT = None
CHARACTER = None
STYLE = None
CARD_TEXT = ('Powers up 6 stages for a personality.')

CARD_POWER = CardPowerNonCombatAttack(NAME, CARD_TEXT, any_power=6)
