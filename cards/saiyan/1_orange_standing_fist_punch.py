import sys

from card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Combat'
NAME = 'Orange Standing Fist Punch'
SUBTYPE = 'Physical Combat - Attack'
SAGA = 'Saiyan'
CARD_NUMBER = '1'
RARITY = 1
CHARACTER = None
STYLE = 'Orange'
CARD_TEXT = ('Physical Attack. Raise card user\'s anger level 1.')

CARD_POWER = CardPowerPhysicalAttack(
    NAME, CARD_TEXT, own_anger=1)
