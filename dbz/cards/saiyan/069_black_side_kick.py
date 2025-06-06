import sys

from card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Combat'
NAME = 'Black Side Kick'
SUBTYPE = 'Physical Combat - Defense'
SAGA = 'Saiyan'
CARD_NUMBER = '69'
RARITY = 3
DECK_LIMIT = None
CHARACTER = None
STYLE = 'Black'
CARD_TEXT = ('Stops a foe\'s physical attack. Raise card user\'s anger level 2.')

CARD_POWER = CardPowerPhysicalDefense(NAME, CARD_TEXT, own_anger=2)
