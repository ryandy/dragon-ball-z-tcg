import sys

from card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Combat'
NAME = 'Black Turning Kick'
SUBTYPE = 'Energy Combat - Attack'
SAGA = 'Saiyan'
CARD_NUMBER = '70'
RARITY = 3
DECK_LIMIT = None
CHARACTER = None
STYLE = 'Black'
CARD_TEXT = ('Energy attack doing 5 life card draws of damage or stops a physical attack.'
             ' Raise card user\'s anger level 1.')

CARD_POWER = [
    CardPowerEnergyAttack(NAME, CARD_TEXT, damage=Damage(life=5), own_anger=1),
    CardPowerPhysicalDefense(NAME, CARD_TEXT, own_anger=1)
]
