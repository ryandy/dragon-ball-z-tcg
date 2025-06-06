import sys

from card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Combat'
NAME = 'Piccolo\'s Energy Attack'
SUBTYPE = 'Energy Combat - Attack'
SAGA = 'Saiyan'
CARD_NUMBER = '109'
RARITY = 3
DECK_LIMIT = None
CHARACTER = 'Piccolo'
STYLE = None
CARD_TEXT = ('Does 6 life card draws of damage and costs 5 stages of power drain to perform.')

CARD_POWER = CardPowerEnergyAttack(
    NAME, CARD_TEXT, damage=Damage.energy_attack(life=6), cost=Cost.energy_attack(power=5))
