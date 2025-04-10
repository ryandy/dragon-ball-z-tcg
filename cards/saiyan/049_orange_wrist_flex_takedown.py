import sys

from card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Combat'
NAME = 'Orange Wrist Flex Takedown'
SUBTYPE = 'Physical Combat - Defense'
SAGA = 'Saiyan'
CARD_NUMBER = '49'
RARITY = 1
DECK_LIMIT = None
CHARACTER = None
STYLE = 'Orange'
CARD_TEXT = ('Stops a physical attack. Raise the card user\'s anger level 1.')

CARD_POWER = CardPowerPhysicalDefense(NAME, CARD_TEXT, own_anger=1)
