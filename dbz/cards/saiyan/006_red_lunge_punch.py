import sys

from card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Combat'
NAME = 'Red Lunge Punch'
SUBTYPE = 'Physical Combat - Attack'
SAGA = 'Saiyan'
CARD_NUMBER = '6'
RARITY = 1
DECK_LIMIT = None
CHARACTER = None
STYLE = 'Red'
CARD_TEXT = ('Physical Attack. Raise card user\'s anger level 1.')

CARD_POWER = CardPowerPhysicalAttack(NAME, CARD_TEXT, own_anger=1)
