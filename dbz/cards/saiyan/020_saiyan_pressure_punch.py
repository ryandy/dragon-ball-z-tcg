import sys

from card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from card_power_defense import CardPowerEnergyDefense, CardPowerPhysicalDefense
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Combat'
NAME = 'Saiyan Pressure Punch'
SUBTYPE = 'Physical Combat - Attack'
SAGA = 'Saiyan'
CARD_NUMBER = '20'
RARITY = 1
DECK_LIMIT = None
CHARACTER = None
STYLE = 'Saiyan'
CARD_TEXT = ('Saiyan Heritage only. Physical attack doing +3 stages of physical damage'
             ' if successful.')

CARD_POWER = CardPowerPhysicalAttack(
    NAME, CARD_TEXT, saiyan_only=True, damage_modifier=DamageModifier(power_add=3))
