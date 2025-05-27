import sys

from card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Combat'
NAME = 'Krillin\'s Energy Disk'
SUBTYPE = 'Energy Combat - Attack'
SAGA = 'Saiyan'
CARD_NUMBER = '216'
RARITY = 5
DECK_LIMIT = None
CHARACTER = 'Krillin'
STYLE = None
CARD_TEXT = ('Energy attack doing 4 life cards of damage at a cost of 1 stage.')

CARD_POWER = CardPowerEnergyAttack(
    NAME, CARD_TEXT, cost=Cost(power=1))
