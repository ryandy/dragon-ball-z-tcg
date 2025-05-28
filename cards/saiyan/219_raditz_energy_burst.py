import sys

from card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Combat'
NAME = 'Raditz Energy Burst'
SUBTYPE = 'Energy Combat - Attack'
SAGA = 'Saiyan'
CARD_NUMBER = '219'
RARITY = 5
DECK_LIMIT = None
CHARACTER = 'Raditz'
STYLE = None
CARD_TEXT = ('Energy attack doing 2 life damage and costing no power stages to perform.')

CARD_POWER = CardPowerEnergyAttack(
    NAME, CARD_TEXT, damage=Damage(life=2), cost=Cost.none())
