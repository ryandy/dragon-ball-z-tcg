import sys

from card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Combat'
NAME = 'Raditz Flying Kick'
SUBTYPE = 'Physical Combat - Attack'
SAGA = 'Saiyan'
CARD_NUMBER = '210'
RARITY = 5
DECK_LIMIT = None
CHARACTER = 'Raditz'
STYLE = None
CARD_TEXT = ('Physical attack doing triple the usual damage if successful.')

CARD_POWER = CardPowerPhysicalAttack(
    NAME, CARD_TEXT, damage_modifier=DamageModifier(power_mult=3))
