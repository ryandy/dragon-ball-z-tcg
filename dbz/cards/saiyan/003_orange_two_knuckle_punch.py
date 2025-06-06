import sys

from card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Combat'
NAME = 'Orange Two Knuckle Punch'
SUBTYPE = 'Physical Combat - Attack'
SAGA = 'Saiyan'
CARD_NUMBER = '3'
RARITY = 1
DECK_LIMIT = None
CHARACTER = None
STYLE = 'Orange'
CARD_TEXT = ('Physical Attack doing +1 stage of damage if successful. Raise card user\'s anger'
             ' level 1.')

CARD_POWER = CardPowerPhysicalAttack(
    NAME, CARD_TEXT, damage_modifier=DamageModifier(power_add=1), own_anger=1)
