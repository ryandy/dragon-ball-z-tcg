import sys

from card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Combat'
NAME = 'Blue Round Throw'
SUBTYPE = 'Physical Combat - Attack'
SAGA = 'Saiyan'
CARD_NUMBER = '13'
RARITY = 1
DECK_LIMIT = None
CHARACTER = None
STYLE = 'Blue'
CARD_TEXT = ('Physical Attack doing +5 stages of damage if successful or stops an'
             ' energy attack. Lower foe\'s anger level 1.')


CARD_POWER = [
    CardPowerPhysicalAttack(
        NAME, CARD_TEXT, damage_modifier=DamageModifier(power_add=5), opp_anger=-1),
    CardPowerEnergyDefense(
        NAME, CARD_TEXT, opp_anger=-1)
]
