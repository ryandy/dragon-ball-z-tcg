import sys

from card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Combat'
NAME = 'Gohan\'s Energy Defense'
SUBTYPE = 'Energy Combat - Defense'
SAGA = 'Saiyan'
CARD_NUMBER = '111'
RARITY = 3
DECK_LIMIT = None
CHARACTER = 'Gohan'
STYLE = None
CARD_TEXT = ('Stops an energy attack. Raise your anger 1 level.')

CARD_POWER = CardPowerEnergyDefense(NAME, CARD_TEXT, own_anger=1)
