import sys

from card_power_on_damage_modification import CardPowerOnDamageModification
from character import Character
from cost import Cost
from damage import Damage
from damage_modifier import DamageModifier


TYPE = 'Drill'
NAME = 'Orange Joint Restraint Drill'
SAGA = 'Saiyan'
CARD_NUMBER = '151'
RARITY = 3
DECK_LIMIT = None
CHARACTER = None
STYLE = 'Orange'
CARD_TEXT = ('All of your physical attacks do +4 power stages of damage.')

CARD_POWER = CardPowerOnDamageModification(
    NAME, CARD_TEXT, own_physical=DamageModifier(power_add=4))
