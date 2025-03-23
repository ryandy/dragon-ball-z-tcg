import sys

from card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Combat'
NAME = 'Gohan\'s Physical Attack'
SUBTYPE = 'Physical Combat - Attack'
SAGA = 'Saiyan'
CARD_NUMBER = '26'
RARITY = 1
DECK_LIMIT = None
CHARACTER = 'Gohan'
STYLE = None
CARD_TEXT = ('Physical attack. Raise your anger 1. Gain 5 power stages.')

CARD_POWER = CardPowerPhysicalAttack(
    NAME, CARD_TEXT, own_anger=1, own_power=5)
