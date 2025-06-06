import sys

from card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Combat'
NAME = 'Black Knife Hand Strike'
SUBTYPE = 'Energy Combat - Attack'
SAGA = 'Saiyan'
CARD_NUMBER = '66'
RARITY = 3
DECK_LIMIT = None
CHARACTER = None
STYLE = 'Black'
CARD_TEXT = ('Energy Attack doing 4 life card draws of damage or stopping any energy attack.')

CARD_POWER = [
    CardPowerEnergyAttack(NAME, CARD_TEXT),
    CardPowerEnergyDefense(NAME, CARD_TEXT)
]
