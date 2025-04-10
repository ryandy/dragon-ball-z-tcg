import sys

from card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Combat'
NAME = 'Raditz Total Defense'
SUBTYPE = 'Physical Combat - Defense'
SAGA = 'Saiyan'
CARD_NUMBER = '47'
RARITY = 1
DECK_LIMIT = None
CHARACTER = 'Raditz'
STYLE = None
CARD_TEXT = ('Stops a physical attack, but costs 1 power stage to perform.')

CARD_POWER = CardPowerPhysicalDefense(NAME, CARD_TEXT, cost=Cost(power=1))
