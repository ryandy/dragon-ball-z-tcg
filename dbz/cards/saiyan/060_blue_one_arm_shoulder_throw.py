import sys

from card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Combat'
NAME = 'Blue One-Arm Shoulder Throw'
SUBTYPE = 'Physical Combat - Defense'
SAGA = 'Saiyan'
CARD_NUMBER = '60'
RARITY = 1
DECK_LIMIT = None
CHARACTER = None
STYLE = 'Blue'
CARD_TEXT = ('Stops the foe\'s physical attack. Lower foe\'s anger level 1.')

CARD_POWER = CardPowerPhysicalDefense(NAME, CARD_TEXT, opp_anger=-1)
