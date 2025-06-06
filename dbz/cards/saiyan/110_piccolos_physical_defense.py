import sys

from card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Combat'
NAME = 'Piccolo\'s Physical Defense'
SUBTYPE = 'Physical Combat - Defense'
SAGA = 'Saiyan'
CARD_NUMBER = '110'
RARITY = 3
DECK_LIMIT = None
CHARACTER = 'Piccolo'
STYLE = None
CARD_TEXT = ('Stops a physical attack. Gain 4 power stages.')

CARD_POWER = CardPowerPhysicalDefense(NAME, CARD_TEXT, any_power=4)
