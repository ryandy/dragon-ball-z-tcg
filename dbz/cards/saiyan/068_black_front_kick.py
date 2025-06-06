import sys

from card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Combat'
NAME = 'Black Front Kick'
SUBTYPE = 'Energy Combat - Attack'
SAGA = 'Saiyan'
CARD_NUMBER = '68'
RARITY = 3
DECK_LIMIT = None
CHARACTER = None
STYLE = 'Black'
CARD_TEXT = ('Energy attack doing 5 life card draws in damage and costing 4 stages of power'
             ' to perform. Raise card user\'s anger level 2.')

CARD_POWER = CardPowerEnergyAttack(
    NAME, CARD_TEXT, damage=Damage(life=5), cost=Cost(power=4), own_anger=2)
